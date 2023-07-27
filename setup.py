import os
import sys
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
from bqx._func_generator import generate_funcpy


here = os.path.abspath(os.path.dirname(__file__))

if 'build' in sys.argv:
    import pypandoc
    with open(os.path.join(here, 'README.md')) as f:
        readme = pypandoc.convert(f.read(), 'rst', format='md')
    with open(os.path.join(here, 'README.rst'), 'w') as f:
        f.write(readme)
else:
    readme = ''

if 'install' in sys.argv or 'test' in sys.argv:
    funcpy_in = os.path.join(here, 'bqx/_func.py')
    funcpy = os.path.join(here, 'bqx/func.py')
    generate_funcpy(funcpy_in, funcpy)

__version__ = '0.4.2'
__license__ = 'BSD License'
__classifiers__ = [
    'Development Status :: 7 - Inactive',
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
]


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
