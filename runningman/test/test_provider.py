# This code is part of runningman.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.
import runningman


def test_backends_kwargs():
    """Test that backends query with kwarg works"""
    provider = runningman.test.PROVIDER
    backends = provider.backends(min_num_qubits=127)
    for backend in backends:
        assert backend.num_qubits >= 127


def test_backends_kwargs2():
    """Test that backends query with impossible kwarg works"""
    provider = runningman.test.PROVIDER
    backends = provider.backends(min_num_qubits=int(1e12))
    assert not any(backends)
