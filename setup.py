# This code is part of runningman.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""RunningMan
"""

import os
import sys
import setuptools


MAJOR = 2
MINOR = 4
MICRO = 0

VERSION = "%d.%d.%d" % (MAJOR, MINOR, MICRO)

with open("requirements.txt") as f:
    REQUIREMENTS = f.read().splitlines()

PACKAGES = setuptools.find_packages()
PACKAGE_DATA = {
}
DOCLINES = __doc__.split("\n")
DESCRIPTION = DOCLINES[0]
this_dir = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_dir, "README.md"), encoding="utf-8") as readme:
    LONG_DESCRIPTION = readme.read()



def write_version_py(filename="runningman/version.py"):
    cnt = """\
# THIS FILE IS GENERATED FROM RUNNINGMAN SETUP.PY
# pylint: disable=missing-module-docstring
version = '%(version)s'
"""
    a = open(filename, "w")
    try:
        a.write(
            cnt
            % {
                "version": VERSION,
            }
        )
    finally:
        a.close()


local_path = os.path.dirname(os.path.abspath(sys.argv[0]))
os.chdir(local_path)
sys.path.insert(0, local_path)
sys.path.insert(0, os.path.join(local_path, "runningman"))  # to retrive _version

# always rewrite _version
if os.path.exists("runningman/version.py"):
    os.remove("runningman/version.py")

write_version_py()

setuptools.setup(
    name="runningman",
    version=VERSION,
    python_requires=">=3.9",
    packages=PACKAGES,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="",
    author="Paul Nation",
    author_email="nonhermitian@gmail.com",
    license="Apache 2.0",
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering",
    ],
    install_requires=REQUIREMENTS,
    package_data=PACKAGE_DATA,
    include_package_data=True,
    zip_safe=False,
)
