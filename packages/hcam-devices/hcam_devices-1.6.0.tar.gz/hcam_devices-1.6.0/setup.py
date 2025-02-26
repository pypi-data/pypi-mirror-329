#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
import glob
import os
import sys

with open("README.rst", encoding="utf-8") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst", encoding="utf-8") as history_file:
    history = history_file.read()

requirements = [
    "astropy",
    "requests",
    "sismic",
    "autobahn",
    "pyserial",
    "twisted",
    "influxdb",
    "txaio",
    "watchdog",
    "six",
]

# for Python 3.6 we need pymodbus3
modern_requirements = ["pymodbus"]
older_requirements = ["pymodbus3"]

test_requirements = [
    # TODO: put package test requirements here
]

# Treat everything in scripts except README.rst as a script to be installed
scripts = [
    fname
    for fname in glob.glob(os.path.join("scripts", "*"))
    if os.path.basename(fname) != "README.rst"
]

setup(
    name="hcam_devices",
    version="1.6.0",
    description="Device Communication via WAMP for HiPerCAM",
    long_description=readme + "\n\n" + history,
    author="Stuart Littlefair",
    author_email="s.littlefair@shef.ac.uk",
    url="https://github.com/HiPERCAM/hcam_devices",
    download_url="https://github.com/HiPERCAM/hcam_devices/archive/v1.6.0.tar.gz",
    packages=[
        "hcam_devices",
        "hcam_devices.gtc",
        "hcam_devices.devices",
        "hcam_devices.components",
        "hcam_devices.machines",
        "hcam_devices.models",
        "hcam_devices.testing",
        "hcam_devices.wamp",
        "hcam_devices.wamp.utils",
        "hcam_devices.utils",
    ],
    package_dir={"hcam_devices": "hcam_devices"},
    include_package_data=True,
    scripts=scripts,
    install_requires=requirements,
    extras_require={
        ':python_version == "3.6"': older_requirements,
        ':python_version >= "3.7"': modern_requirements,
    },
    license="MIT license",
    zip_safe=False,
    keywords="hcam_devices",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
    ],
    test_suite="tests",
    tests_require=test_requirements,
)
