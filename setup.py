# ----------------------------------------------------------------------------
# Copyright (c) 2020, Franck Lejzerowicz.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import re, ast
from setuptools import find_packages, setup

classes = """
    License :: OSI Approved :: BSD License
    Topic :: Scientific/Engineering
    Topic :: Scientific/Engineering :: Bio-Informatics
    Programming Language :: Python :: 3.6
    Programming Language :: Python :: 3 :: Only
    Operating System :: Unix
    Operating System :: POSIX
    Operating System :: MacOS :: MacOS X
"""

classifiers = [s.strip() for s in classes.split('\n') if s]

description = (
    "Xplor_distros is a command line tool that allows"
    "looking at the distributions of the numeric"
    "variables in a metadata file."
)

with open("README.md") as f:
    long_description = f.read()

_version_re = re.compile(r"__version__\s+=\s+(.*)")

with open("Xplor_distros/__init__.py", "rb") as f:
    hit = _version_re.search(f.read().decode("utf-8")).group(1)
    version = str(ast.literal_eval(hit))

standalone = ['Xplor_distros=Xplor_distros.scripts._standalone_xplor:standalone_xplor']

setup(
    name="Xplor_distros",
    version=version,
    license="BSD",
    description=description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Franck Lejzerowicz",
    author_email="franck.lejzerowicz@gmail.com",
    maintainer="Franck Lejzerowicz",
    maintainer_email="franck.lejzerowicz@gmail.com",
    url="https://github.com/FranckLejzerowicz/Xplor_distros",
    packages=find_packages(),
    install_requires=[
        "click",
        'numpy >= 1.12.1',
        'scipy >= 0.19.1',
        'pandas >= 0.10.0',
        'altair >= 3.2.0',
        "matplotlib"
    ],
    classifiers=classifiers,
    entry_points={'console_scripts': standalone},
    package_data={
        'Xplor_distros': ['tests/*/*'],
    },
    include_package_data=True,
    python_requires='>=3.6',
)
