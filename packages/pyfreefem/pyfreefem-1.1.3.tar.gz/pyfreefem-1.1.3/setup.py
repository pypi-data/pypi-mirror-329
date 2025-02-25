# Copyright 2018-2019 CNRS, Ecole Polytechnique and Safran.
#
# This file is part of pyfreefem.
#
# nullspace_optimizer is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# nullspace_optimizer is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# A copy of the GNU General Public License is included below.
# For further information, see <http://www.gnu.org/licenses/>.

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyfreefem",
    version="1.1.3",
    author="Florian Feppon",
    author_email="florian.feppon@kuleuven.be",
    license="GNU GPL version 3",
    description="Package PyFreeFEM for interfacing Python and FreeFEM.",
    keywords="FreeFEM",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://pyfreefem.readthedocs.io/en/latest/",
    packages=setuptools.find_packages(),
    package_data={'':['*.edp','*/*.edp']},    
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Mathematics"
    ],
    install_requires=['numpy>=1.12.1',
                      'scipy>=0.19.1',  
                      'colored>=1.3.93',    
                      'pymedit>=1.2'],
    python_requires='>=3.6',
)
