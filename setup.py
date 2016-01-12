import os
import sys
from codecs import open
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    readme = f.read()

__version__ = '0.0.1'
__author__ = 'Takumi Sueda'
__author_email__ = 'takumi.sueda@fuller.co.jp'
__license__ = 'BSD License'
__classifiers__ = (
    'Development Status :: 2 - Pre-Alpha',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: SQL',
    'Topic :: Database',
    'Topic :: Software Development :: Code Generators'
)


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        pytest.main(self.test_args)

setup(
    name='bqx',
    version=__version__,
    author=__author__,
    author_email=__author_email__,
    url='https://github.com/fuller-inc/bqx',
    description='Generate sophisticated query for Google BigQuery in simple way.',
    long_description=readme,
    classifiers=__classifiers__,
    packages=find_packages(exclude=['test*']),
    license=__license__,
    include_package_data=True,
    test_suite='tests',
    tests_require=['pytest'],
    cmdclass={'test': PyTest},
)
