# -*- coding: utf-8 -*-
"""Packaging logic for blurtpy."""
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

VERSION = '0.24.22'

tests_require = ['mock >= 2.0.0', 'pytest', 'pytest-mock', 'parameterized']

requires = [
    "ecdsa",
    "requests",
    "websocket-client",
    "appdirs",
    "scrypt",
    "pycryptodomex",
    "pytz",
    "Click",
    "click_shell",
    "prettytable",
    "ruamel.yaml",
    "diff_match_patch",
    "asn1crypto"
]


def write_version_py(filename):
    """Write version."""
    cnt = """\"""THIS FILE IS GENERATED FROM blurtpy SETUP.PY.\"""
version = '%(version)s'
"""
    with open(filename, 'w') as a:
        a.write(cnt % {'version': VERSION})


def get_long_description():
    """Generate a long description from the README file."""
    descr = []
    for fname in ('README.md',):
        with io.open(fname, encoding='utf-8') as f:
            descr.append(f.read())
    return '\n\n'.join(descr)


if __name__ == '__main__':

    # Rewrite the version file everytime
    write_version_py('blurtpy/version.py')
    write_version_py('blurtbase/version.py')
    write_version_py('blurtapi/version.py')
    write_version_py('blurtgraphenebase/version.py')

    setup(
        name='blurtpy',
        version=VERSION,
        description='Python library for Blurt blockchain',
        long_description=get_long_description(),
        long_description_content_type='text/markdown',
        download_url='https://gitlab.com/blurt/blurtpy/tarball/' + VERSION,
        author='Blurt Community',
        author_email='dev@blurt.blog',
        maintainer='Blurt Community',
        maintainer_email='dev@blurt.blog',
        url='https://gitlab.com/blurt/blurtpy',
        keywords=['blurt', 'blockchain', 'library', 'api', 'rpc'],
        packages=[
            "blurtpy",
            "blurtapi",
            "blurtbase",
            "blurtgraphenebase",
            "blurtgrapheneapi",
            "blurtstorage"
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
                'blurtpy=blurtpy.cli:cli',
            ],
        },
        setup_requires=['pytest-runner'],
        tests_require=tests_require,
        include_package_data=True,
    )
