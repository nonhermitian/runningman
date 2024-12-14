# This code is part of runningman.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""RunningMan mode
"""
from qiskit_ibm_runtime import Session


class RunningManMode(Session):
    """General mode class unifying Batch and Session
    """
    def __init__(self, mode):
        self.mode = mode
        self.jobs = []
        self.mode_name = mode.details()['mode']
        self.mode_id = self.mode.session_id
        self.backend = None
        if isinstance(mode, RunningManMode):
            self.backend = mode.backend
        else:
            from runningman.backend import RunningManBackend
            backend = self.service.backend(mode.backend())
            self.backend = RunningManBackend(backend)

        # For iterating through jobs list
        self._iter_index = 0

    def __getattr__(self, attr):
        if attr in self.__dict__:
            return self.__dict__[attr]
        return getattr(self.mode, attr)

    def __repr__(self):
        out_str = f"<RunningManMode('{self.mode_name}', mode_id='{self.mode_id}'>"
        return out_str

    def __len__(self):
        return len(self.jobs)

    def __getitem__(self, item):
        return self.jobs[item]

    def __iter__(self):
        self._iter_index = 0
        return self
    
    def __next__(self):
        if self._iter_index < len(self):
            self._iter_index += 1
            return self.jobs[self._iter_index-1]
        else:
            raise StopIteration
