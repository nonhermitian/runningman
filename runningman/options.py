# This code is part of runningman.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""RunningMan options
"""
from qiskit_ibm_runtime import SamplerOptions


class ExecutionOptions(dict):
    def __repr__(self):
        # Find max key length
        max_length = 0
        for val in self.values():
            for item in val:
                max_length = max(max_length, len(item))

        indent = 0
        out = "Execution Options\n"
        out += "=" * 40 + "\n"
        for key, val in self.items():
            indent = 0
            out += "\u23F5" + key + "\n"
            indent = 2
            for item, entry in val.items():
                out += (
                    " " * indent
                    + item
                    + " " * (max_length - len(item) + 5)
                    + str(entry)
                    + "\n"
                )
        return out


def default_execution_options():
    """Return a default set of execution options"""
    out = ExecutionOptions(
        {
            "execution": {
                "default_shots": 4096,
                "experimental": None,
                "init_qubits": None,
                "max_execution_time": None,
                "meas_type": None,
                "rep_delay": None,
            },
            "environment": {
                "log_level": "WARNING",
                "callback": None,
                "job_tags": None,
                "private": False,
            },
            "simulator": {
                "noise_model": None,
                "seed_simulator": None,
                "coupling_map": None,
                "basis_gates": None,
            },
        }
    )

    return out


def build_sampler_options(execution_options):
    """Build a SamplerOptions object from RunningMan options

    Parameters:
        execution_options (ExecutionOptions): Execution options

    Returns:
        SamplerOptions
    """
    execution_options = _deflate_options_dict(execution_options)
    out = SamplerOptions()
    for item, val in execution_options["execution"].items():
        out.__dict__[item] = val
    out.update(environment=execution_options["environment"])
    out.update(simulator=execution_options["simulator"])
    return out


def _deflate_options_dict(options):
    """Return a dict with all None values removed

    Parameters:
        options (dict): Input options dict

    Returns:
        dict: Output dict with None values removed
    """
    out = {}
    for key in options:
        out[key] = {}
        for item, val in options[key].items():
            if val is not None:
                out[key][item] = val
    return out
