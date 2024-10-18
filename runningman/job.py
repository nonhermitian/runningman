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


class RunningManJob:
    """A wrapper around Sampler jobs that allows for getting counts from backend.run

    Unlike the Runtime, the results are cached
    """

    def __init__(self, job, executor):
        self.job = job
        if executor not in ["sampler", "estimator"]:
            raise ValueError("executor must be one of 'sampler' or 'estimator'")
        self.executor = executor
        self._result = None  # cache the job result

    def __getattr__(self, attr):
        if attr in self.__dict__:
            return self.__dict__[attr]
        return getattr(self.job, attr)

    def result(self):
        """Get the result from a job

        Adds a `get_counts` attr for backward compatibility

        Returns:
            PrimitiveResult
        """
        if self._result:
            return self._result
        else:
            res = self.job.result()
            setattr(res, "get_counts", _get_counts)
            res.get_counts = types.MethodType(_get_counts, res)
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
    """Internal method to convert Runtime results to backend.run results"""
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
        out_data = {}
        for key, val in combined_counts.items():
            out_data[" ".join(chunkstring(key, chunks))] = val
        out.append(Counts(out_data))
    if len(out) == 1:
        return out[0]
    return out
