# This code is part of runningman.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""RunningMan provider
"""
from qiskit_ibm_runtime import QiskitRuntimeService

from runningman.backend import RunningManBackend


class RunningManProvider:
    """A provider that impliments the RunningMan interfaces"""

    def __init__(self, *args, **kwargs):
        self.service = QiskitRuntimeService(*args, **kwargs)

    def backend(self, name):
        backend = self.service.backend(name)
        return RunningManBackend(backend)

    def backends(self):
        backend_list = self.service.backends()
        return [RunningManBackend(back) for back in backend_list]
