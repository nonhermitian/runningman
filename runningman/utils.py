# This code is part of runningman.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""RunningMan utilities"""
from qiskit_ibm_runtime import IBMBackend

from runningman.backend import RunningManBackend


def is_ibm_backend(backend):
    """Check if a backend is an IBM backend but not a RunningManBackend

    Simplifes instance checking in packages

    Parameters:
        backend (BackendV2 or BackendV1): A backend instance

    Returns:
        bool: True if backend is from IBM
    """
    if isinstance(backend, IBMBackend) and not isinstance(backend, RunningManBackend):
        return True
    return False


def easy_wrap(backend):
    """Easily wrap IBM backends only

    Passes through any backend that is NOT and IBM device

    Parameters:
        backend (BackendV2 or BackendV1): A backend instance

    Returns:
        RunningManBackend: If input is an IBM backend
        BackendV2 or BackendV1: If input is NOT an IBM backend
    """
    if is_ibm_backend(backend):
        return RunningManBackend(backend)
    return backend
