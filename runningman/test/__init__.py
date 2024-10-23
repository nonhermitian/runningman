# This code is part of runningman.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.
import os
import runningman as rm


PROVIDER = rm.RunningManProvider()
# Get backend from env var or default to open Brisbane
BACKEND = PROVIDER.backend(os.environ.get("RM_BACKEND", "ibm_brisbane"))
# holder for a job id used across tests
TEMP_JOB_ID = None
