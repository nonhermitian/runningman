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
                "max_execution_time": None,
                "default_shots": 4096,
                "experimental": None,
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
