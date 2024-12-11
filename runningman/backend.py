# This code is part of runningman.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""RunningMan backend
"""
import copy
from collections.abc import Iterable
from qiskit_ibm_runtime import Batch, Session, SamplerV2, EstimatorV2, IBMBackend

from runningman.job import RunningManJob
from runningman.options import (
    default_execution_options,
    default_suppression_options,
    build_sampler_options,
)

SAMPLER = SamplerV2
ESTIMATOR = EstimatorV2


class RunningManBackend(IBMBackend):
    def __init__(self, backend):
        self.backend = backend
        self._mode = None
        self._execution_options = default_execution_options()
        self._suppression_options = default_suppression_options()

    def __getattr__(self, attr):
        if attr in self.__dict__:
            return self.__dict__[attr]
        return getattr(self.backend, attr)

    def __repr__(self):
        out_str = f"RunningManBackend<name='{self.name}', num_qubits={self.num_qubits}, instance='{self._instance}'>"
        return out_str

    def set_mode(self, mode, overwrite=False):
        """Set the execution mode for jobs from the backend

        Parameters:
            mode (str or Batch or Session): The mode to use for executing jobs
            overwrite (bool): Allow for overwriting a mode without clearing it first

        Returns:
            Batch: If mode is a batch
            Session: If mode is a session
        """
        if self._mode and not overwrite:
            raise Exception(
                "backend mode is already set.  use overwrite=True or clear the mode"
            )
        if self._mode:
            self.close_mode()
        if mode == "batch":
            mode = Batch(backend=self.backend)
            self._mode = mode
        elif mode == "session":
            mode = Session(backend=self.backend)
            self._mode = mode
        elif isinstance(mode, (Batch, Session)):
            if mode.backend() != self.backend.name:
                raise Exception(
                    f"Input mode does not target backend {self.backend.name}"
                )
            self._mode = mode
        else:
            return getattr(self.backend, mode)
        return self._mode

    def get_mode(self):
        """Return the current backend mode

        Returns:
            Batch: If mode is batch
            Session: If mode is session
            None: If no mode is set
        """
        return self._mode

    def close_mode(self):
        """Close the current backend mode, if any"""
        if self._mode:
            self._mode.close()
        else:
            raise Exception("No mode to close")

    def clear_mode(self):
        """Clear the current mode from the backend
        
        Will close any mode that currently exists.

        """
        if self._mode:
            self._mode.close()
        self._mode = None

    def get_sampler(self):
        """Return a sampler object that uses the backend and mode

        Returns:
            SamplerV2: Sampler targeting backend in the current execution mode
        """
        sampler_options = build_sampler_options(
            self.get_execution_options(), self.get_suppression_options()
        )
        return SAMPLER(
            mode=self._mode if self._mode else self.backend, options=sampler_options
        )

    def get_estimator(self):
        """Return an estimator object that uses the backend and mode

        Returns:
            EstimatorV2: Estimator targeting backend in the current execution mode
        """
        return ESTIMATOR(mode=self._mode if self._mode else self.backend)

    def get_execution_options(self):
        """Return the backend's execution options

        Returns:
            ExecutionOptions: A dict specifying execution options
        """
        return copy.deepcopy(self._execution_options)

    def get_suppression_options(self):
        """Return the backend's error suppression options

        Returns:
            SuppressionOptions: A dict specifying execution options
        """
        return copy.deepcopy(self._suppression_options)

    def set_execution_options(self, execution=None, environment=None, simulator=None):
        """Set the execution options of the backend

        Parameters:
            execution (dict): Dict of execution options
            environment (dict): Dict of environment options
            simulator (dict): Dict of simulator options
        """
        if execution and not isinstance(execution, dict):
            raise TypeError("execution is not a dict")
        if environment and not isinstance(environment, dict):
            raise TypeError("environment is not a dict")
        if simulator and not isinstance(simulator, dict):
            raise TypeError("simulator is not a dict")

        if execution:
            for key, val in execution.items():
                if key not in self._execution_options["execution"]:
                    raise KeyError(f"Execution option {key} is not valid")
                self._execution_options["execution"][key] = val

        if environment:
            for key, val in environment.items():
                if key not in self._execution_options["environment"]:
                    raise KeyError(f"Environment option {key} is not valid")
                self._execution_options["environment"][key] = val

        if simulator:
            for key, val in simulator.items():
                if key not in self._execution_options["simulator"]:
                    raise KeyError(f"Simulator option {key} is not valid")
                self._execution_options["simulator"][key] = val

    def set_suppresion_options(self, dynamical_decoupling=None, twirling=None):
        """Set the suppression options of the backend

        Parameters:
            dynamical_decoupling (dict): Dict of dynamical decoupling options
            twirling (dict): Dict of Pauli twirling options
        """
        if dynamical_decoupling and not isinstance(dynamical_decoupling, dict):
            raise TypeError("dynamical_decoupling is not a dict")
        if twirling and not isinstance(twirling, dict):
            raise TypeError("twirling is not a dict")

        if dynamical_decoupling:
            for key, val in dynamical_decoupling.items():
                if key not in self._suppression_options["dynamical_decoupling"]:
                    raise KeyError(f"Dynamical_decoupling option {key} is not valid")
                self._suppression_options["dynamical_decoupling"][key] = val

        if twirling:
            for key, val in twirling.items():
                if key not in self._suppression_options["twirling"]:
                    raise KeyError(f"Twirling option {key} is not valid")
                self._suppression_options["twirling"][key] = val

    def reset_options(self):
        """Reset all options to default values"""
        self._execution_options = default_execution_options()
        self._suppresion_options = default_suppression_options()

    def run(
        self,
        circuits,
        shots=None,
        job_tags=None,
        rep_delay=None,
        init_qubits=True,
        **kwargs,
    ):
        """Standard Qiskit run mode

        Parameters:
            shots (int): The number of shots per circuit
            job_tags (list): A list of str job tags
            rep_delay (float): A custom rep delay in between circuits
            init_qubits (bool): Initialize qubits between shots, default=True
        """
        sampler = self.get_sampler()
        sampler.options.execution.init_qubits = init_qubits
        if rep_delay:
            sampler.options.execution.rep_delay = rep_delay
        sampler.options.environment.job_tags = job_tags
        if not isinstance(circuits, Iterable):
            circuits = [circuits]
        job = sampler.run(circuits, shots=shots)
        return RunningManJob(job)
