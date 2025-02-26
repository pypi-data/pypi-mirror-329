# SPDX-FileCopyrightText: 2025 Technische Universität Dresden, Germany <tu-dresden.de/zih>
# SPDX-License-Identifier: BSD-3-Clause

from setuptools import setup, find_packages

setup(
    name='snakemake_wfcommons',
    version='0.1.0',
    description='Python tool to convert Snakemake metadata to wfcommons single JSON files',
    url='https://github.com/tud-zih-tools/snakemake-wfcommons',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: BSD License'
    ],
    packages=find_packages(include=['snakemake_wfcommons', 'snakemake_wfcommons.*']),
    scripts=['bin/wfcommons-converter'],
    install_requires=[
        'wfcommons==1.0',
        'snakemake'
    ]
)
