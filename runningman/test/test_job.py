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
import runningman as rm
import runningman.test


def test_job_retrieval():
    """Test that a job has the correct properties"""
    provider = runningman.test.PROVIDER
    job = provider.job(runningman.test.TEMP_JOB_ID)
    assert job.backend().name == runningman.test.BACKEND.name
    assert isinstance(job, rm.job.RunningManJob)
    counts = job.result().get_counts()
    assert sum(counts.values()) == 1234
    assert len(next(iter(counts))) == 5
