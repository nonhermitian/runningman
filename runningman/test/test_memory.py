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
from runningman.test import BACKEND


def test_run_memory1():
    """Test getting memory from a job"""
    qc = QuantumCircuit(5)
    qc.h(2)
    qc.cx(2,1)
    qc.cx(1,0)
    qc.cx(2,3)
    qc.cx(3,4)
    qc.measure_all()

    trans_qc = transpile(qc, BACKEND)
    job = BACKEND.run(trans_qc, shots=135)
    
    memory = job.result().get_memory()
    assert len(memory) == 135
    assert len(memory[0]) == 5


def test_run_memory2():
    """Test getting memory from a job with two cregs"""
    qr = QuantumRegister(5)
    cr1 = ClassicalRegister(2)
    cr2 = ClassicalRegister(3)
    qc = QuantumCircuit(qr, cr1, cr2)
    qc.h(2)
    qc.cx(2,1)
    qc.cx(1,0)
    qc.cx(2,3)
    qc.cx(3,4)
    qc.measure([0,1], cr1)
    qc.measure([2,3,4], cr2)

    trans_qc = transpile(qc, BACKEND)
    job = BACKEND.run(trans_qc, shots=135)
    memory = job.result().get_memory()
    assert len(memory) == 135
    key_chunks = memory[0].split(' ')
    assert len(key_chunks[0]) == 3
    assert len(key_chunks[1]) == 2
