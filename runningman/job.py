# This code is part of runningman.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""RunningMan job
"""
import types
from qiskit.result import Counts
from qiskit.primitives.containers import SamplerPubResult


class RunningManJob:
    """A wrapper around Sampler jobs that allows for getting counts from backend.run

    Unlike the Runtime, the results are cached
    """

    def __init__(self, job):
        self.job = job
        self._result = None  # cache the job result
        self.executor = None

    def __getattr__(self, attr):
        if attr in self.__dict__:
            return self.__dict__[attr]
        return getattr(self.job, attr)

    def __repr__(self):
        job_id = self.job.job_id()
        backend_name = self.job.backend().name
        executor = self.executor if self.executor else "NA"
        out_str = f"RunningManJob<job_id='{job_id}', backend_name='{backend_name}', executor='{executor}'>"
        return out_str

    def result(self):
        """Get the result from a job

        Adds a `get_counts` and `get_memory` attr for backward compatibility

        Returns:
            PrimitiveResult
        """
        if self._result:
            return self._result
        else:
            res = self.job.result()
            if isinstance(res[0], SamplerPubResult):
                setattr(res, "get_counts", _get_counts)
                res.get_counts = types.MethodType(_get_counts, res)
                setattr(res, "get_memory", _get_memory)
                res.get_memory = types.MethodType(_get_memory, res)
                self.executor = "sampler"
            else:
                self.executor = "estimator"
            self._result = res
            return res


def chunkstring(string, lengths):
    """Breaks up a string across classical register lengths

    Parameters:
        string (str): Input string
        lengths (list): List of lengths to slice over

    Returns:
        Generator
    """
    return (
        string[pos : pos + length].strip()
        for idx, length in enumerate(lengths)
        for pos in [sum(map(int, lengths[:idx]))]
    )


def _get_counts(self, experiment=None):
    """Get the histogram data of an experiment.

    Parameters:
        experiment (int or None): Index of the experiment, default=None

    Returns:
        dict : Counts for a single experiment
        list : List of dicts for each experiment in a multi-circuit job
    """
    if experiment is None:
        exp_keys = range(len(self))
    else:
        exp_keys = [experiment]
    out = []
    for idx in exp_keys:
        item = self[idx]
        combined_counts = item.join_data().get_counts()
        chunks = [item[1].num_bits for item in item.data.items()][
            ::-1
        ]  # This is reversed for LSB ordering
        if len(chunks) > 1:
            out_data = {}
            for key, val in combined_counts.items():
                out_data[" ".join(chunkstring(key, chunks))] = val
            out.append(Counts(out_data))
        else:
            out.append(Counts(combined_counts))
    if len(out) == 1:
        return out[0]
    return out


def _get_memory(self, experiment=None):
    """Get the sequence of memory states (readouts) for each shot

    Parameters:
        experiment (int or None): Index of the experiment, default=None

    Returns:
        list: List of strings representing the bitstrings for each shot
    """
    if experiment is None:
        exp_keys = range(len(self))
    else:
        exp_keys = [experiment]
    out = []
    for idx in exp_keys:
        item = self[idx]
        combined_samples = item.join_data().get_bitstrings()
        chunks = [item[1].num_bits for item in item.data.items()][
            ::-1
        ]  # This is reversed for LSB ordering
        if len(chunks) > 1:
            out_data = []
            for bitstring in combined_samples:
                out_data.append(" ".join(chunkstring(bitstring, chunks)))
            out.append(out_data)
        else:
            out.append(combined_samples)
    if len(out) == 1:
        return out[0]
    return out
