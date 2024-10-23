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
from runningman.job import RunningManJob


class RunningManProvider:
    """A provider that impliments the RunningMan interfaces"""

    def __init__(self, *args, **kwargs):
        self.service = QiskitRuntimeService(*args, **kwargs)

    def __getattr__(self, attr):
        if attr in self.__dict__:
            return self.__dict__[attr]
        return getattr(self.service, attr)

    def backend(self, name):
        backend = self.service.backend(name)
        return RunningManBackend(backend)

    def backends(self):
        backend_list = self.service.backends()
        return [RunningManBackend(back) for back in backend_list]

    def job(self, job_id):
        """Return a specific job given a job_id

        Parameters:
            job_id (str): A job ID string

        Returns:
            RunningManJob: The requested job instance in RunningMan format
        """
        job = self.service.job(job_id)
        return RunningManJob(job)

    def jobs(self, *args, **kwargs):
        """Retrieve runtime jobs with filtering.

        Input arguments are the same as `QiskitRuntimeService.jobs()`

        Returns:
            list: A list of RunnningManJobs
        """
        jobs = self.service.jobs(*args, **kwargs)
        return [RunningManJob(job) for job in jobs]
