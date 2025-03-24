# -*- coding: utf-8 -*-
"""Packaging logic for beem."""
import codecs
import io
import os
import sys

from setuptools import setup

# Work around mbcs bug in distutils.
# http://bugs.python.org/issue10945

try:
    codecs.lookup('mbcs')
except LookupError:
    ascii = codecs.lookup('ascii')
    codecs.register(lambda name, enc=ascii: {True: enc}.get(name == 'mbcs'))

VERSION = '0.26.1'

tests_require = [
    "mock == 4.0.3",
    "pytest == 7.2.2",
    "pytest-mock == 3.12.0",
    "parameterized == 0.9.0",
    "setuptools == 77.0.3",
    "wheel == 0.42.0",
    "future == 0.18.2",
    "cryptography == 3.4.7",
    "pycodestyle == 2.7.0",
    "pyflakes == 2.3.1",
    "pylibscrypt == 2.0.0",
    "six == 1.17.0",
    "pytest-cov == 4.1.0",
    "coverage == 7.4.3",
    "tox == 4.13.0",
    "codacy-coverage == 1.3.11",
    "virtualenv == 20.25.1",
]

requires = [
    "ecdsa == 0.19.1",
    "requests >= 2.31.0",
    "websocket-client >= 1.6.3",
    "appdirs == 1.4.4",
    "scrypt == 0.8.18",
    "pycryptodomex == 3.10.1",
    "pytz == 2021.1",
    "Click == 8.0.0",
    "click_shell == 2.1",
    "prettytable == 3.8.0",
    "ruamel.yaml == 0.18.6",
    "diff_match_patch == 20230430",
    "asn1crypto == 1.5.1"
]


def write_version_py(filename):
    """Write version."""
    cnt = """\"""THIS FILE IS GENERATED FROM beem SETUP.PY.\"""
version = '%(version)s'
"""
    with open(filename, 'w') as a:
        a.write(cnt % {'version': VERSION})


def get_long_description():
    """Generate a long description from the README file."""
    descr = []
    for fname in ('README.rst',):
        with io.open(fname, encoding='utf-8') as f:
            descr.append(f.read())
    return '\n\n'.join(descr)


if __name__ == '__main__':

    # Rewrite the version file everytime
    write_version_py('beem/version.py')
    write_version_py('beembase/version.py')
    write_version_py('beemapi/version.py')
    write_version_py('beemgraphenebase/version.py')

    setup(
        name='beem',
        version=VERSION,
        description='Unofficial Python library for HIVE',
        long_description=get_long_description(),
        download_url='https://github.com/holgern/beem/tarball/' + VERSION,
        author='Holger Nahrstaedt',
        author_email='nahrstaedt@gmail.com',
        maintainer='Holger Nahrstaedt',
        maintainer_email='nahrstaedt@gmail.com',
        url='http://www.github.com/holgern/beem',
        keywords=['hive', 'library', 'api', 'rpc'],
        packages=[
            "beem",
            "beemapi",
            "beembase",
            "beemgraphenebase",
            "beemgrapheneapi",
            "beemstorage"
        ],
        classifiers=[
            'License :: OSI Approved :: MIT License',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
            'Development Status :: 4 - Beta',
            'Intended Audience :: Developers',
            'Intended Audience :: Financial and Insurance Industry',
            'Topic :: Office/Business :: Financial',
        ],
        install_requires=requires,
        entry_points={
            'console_scripts': [
                'beempy=beem.cli:cli',
            ],
        },
        setup_requires=['pytest-runner'],
        tests_require=tests_require,
        extras_require={"tests": tests_require},
        include_package_data=True,
    )
