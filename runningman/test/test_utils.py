# This code is part of runningman.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.
from qiskit import *
from qiskit_ibm_runtime.fake_provider import FakeAthensV2

from runningman.test import BACKEND
from runningman.utils import is_ibm_backend


def test_test_is_ibm():
    """Verify IBM backend check works"""
    assert is_ibm_backend(BACKEND) == True


def test_test_not_ibm():
    """Verify IBM backend check returns False is not IBM backend"""
    backend = FakeAthensV2()
    assert not is_ibm_backend(backend)
