#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

import os
import sys

from distutils.command.build_scripts import build_scripts
from distutils import util, log

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['numpy']

setup_requirements = []

test_requirements = ['pytest>=3.5.0']

class build_scripts_rename(build_scripts):
    def copy_scripts(self):
        build_scripts.copy_scripts(self)
        # remove the .py extension from scripts
        for s in self.scripts:
            f = util.convert_path(s)
            before = os.path.join(self.build_dir, os.path.basename(f))
            after = os.path.splitext(before)[0]
            log.info("renaming %s -> %s" % (before, after))
            os.rename(before, after)


cmdclass = {
    'build_scripts': build_scripts_rename,
}


setup(
    author="Oishe Farhan",
    author_email='oishe.farhan@interaxon.ca',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="Python scripts to capture and replay OSC packets. Built on top of pyliblo.",
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='osc_recorder',
    name='osc_recorder',
    packages=find_packages(include=['osc_recorder']),
    scripts=['scripts/capture_osc.py', 'scripts/replay_osc.py'],
    cmdclass=cmdclass,
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/oishefarhan/osc_recorder',
    version='0.1.2',
    zip_safe=False,
)
