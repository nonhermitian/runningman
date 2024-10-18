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
from collections.abc import Iterable
from qiskit_ibm_runtime import Batch, Session, SamplerV2, EstimatorV2

from runningman.job import RunningManJob


SAMPLER = SamplerV2
ESTIMATOR = EstimatorV2


class RunningManBackend:
    def __init__(self, backend):
        self.backend = backend
        self._mode = None

    def __getattr__(self, attr):
        if attr in self.__dict__:
            return self.__dict__[attr]
        return getattr(self.backend, attr)

    def __repr__(self):
        out_str = f"RunningManBackend<name='{self.name}', num_qubits={self.num_qubits}, instance='{self._instance}'>"
        return out_str

    def set_mode(self, mode, overwrite=False):
        if self._mode and not overwrite:
            raise Exception(
                "backend mode is already set.  use overwrite=True or clear the mode"
            )
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
        return self._mode

    def close_mode(self):
        if self._mode:
            self._mode.close()
        else:
            raise Exception("No mode to close")

    def clear_mode(self):
        self._mode = None

    def get_sampler(self):
        return SAMPLER(mode=self._mode if self._mode else self.backend)

    def get_estimator(self):
        return ESTIMATOR(mode=self._mode if self._mode else self.backend)

    def run(
        self, circuits, shots=None, job_tags=None, rep_delay=None, init_qubits=True, **kwargs
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
        if job_tags:
            job_tags.append("\u2003")
        else:
            job_tags = ["\u2003"]
        sampler.options.environment.job_tags = job_tags
        if not isinstance(circuits, Iterable):
            circuits = [circuits]
        job = sampler.run(circuits, shots=shots)
        return RunningManJob(job, executor="sampler")
