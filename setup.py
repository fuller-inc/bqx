import os
import sys
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
from bqx._func_generator import generate_funcpy


here = os.path.abspath(os.path.dirname(__file__))

if 'register' in sys.argv:
    import pypandoc
    with open(os.path.join(here, 'README.md')) as f:
        readme = pypandoc.convert(f.read(), 'rst', format='md')
else:
    readme = ''

if 'install' in sys.argv or 'test' in sys.argv:
    funcpy_in = os.path.join(here, 'bqx/_func.py')
    funcpy = os.path.join(here, 'bqx/func.py')
    generate_funcpy(funcpy_in, funcpy)

__version__ = '0.3.0'
__author__ = 'Takumi Sueda'
__author_email__ = 'takumi.sueda@fuller.co.jp'
__license__ = 'BSD License'
__classifiers__ = (
    'Development Status :: 4 - Beta',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'Intended Audience :: Science/Research',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: SQL',
    'Topic :: Database',
    'Topic :: Software Development :: Code Generators',
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
    description='Query generator for Google BigQuery and other SQL environments',
    long_description=readme,
    classifiers=__classifiers__,
    packages=find_packages(exclude=['test*']),
    license=__license__,
    include_package_data=True,
    test_suite='tests',
    tests_require=['pytest'],
    cmdclass={'test': PyTest},
)
