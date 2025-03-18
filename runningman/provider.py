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
from qiskit_ibm_runtime import QiskitRuntimeService, Batch, Session

from runningman.backend import RunningManBackend
from runningman.job import RunningManJob
from runningman.mode import RunningManMode

_CHUNK_SIZE = 50


class RunningManProvider:
    """A provider that impliments the RunningMan interfaces"""

    def __init__(self, *args, **kwargs):
        self.service = QiskitRuntimeService(*args, **kwargs)

    def __getattr__(self, attr):
        if attr in self.__dict__:
            return self.__dict__[attr]
        return getattr(self.service, attr)

    def backend(self, name, *args, **kwargs):
        """Get an instance of a backend"""
        backend = self.service.backend(name, *args, **kwargs)
        return RunningManBackend(backend)

    def backends(self, *args, **kwargs):
        """List available backends, with optional filtering"""
        backend_list = self.service.backends(*args, **kwargs)
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

    def mode_from_id(self, mode_id):
        """Return a RunningManMode from a given ID

        Parameters:
            mode_id (str): The mode ID

        Returns:
            RunningManMode: The mode instance
        """
        response = self._api_client.session_details(mode_id)
        mode = response.get("mode")
        if mode == "batch":
            temp_mode = Batch.from_id(mode_id, self)
        elif mode == "dedicated":
            temp_mode = Session.from_id(mode_id, self)
        else:
            raise Exception(f"Invalid mode {mode} returned")

        out = RunningManMode(temp_mode)
        out.jobs = fetch_mode_jobs(mode_id, self)
        return out


def fetch_mode_jobs(mode_id, provider):
    """Get the jobs for a given mode"""
    jobs = []
    finished = False
    iter = 0
    while not finished:
        temp_jobs = provider.jobs(
            session_id=mode_id, limit=_CHUNK_SIZE, skip=iter * _CHUNK_SIZE
        )
        jobs.extend(temp_jobs)
        if len(temp_jobs) < _CHUNK_SIZE:
            finished = True
        iter += 1
    return [RunningManJob(jj) for jj in jobs[::-1]]
