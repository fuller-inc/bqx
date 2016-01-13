"""
Test of bqx.func.

Run Test: `tox` or `python setup.py test`
"""

from bqx.parts import Column
from bqx.func import _fn_factory
from bqx.func import CAST, CONCAT


funcs = ['COUNT', 'SUM', 'INTEGER', 'SQRT', 'IF', 'POW']
column = Column('column').AS('col')


def test_cast():
    assert str(CAST('type1', 'type2')) == 'CAST(type1 AS type2)'


def test_concat():
    assert str(CONCAT('a', 'b', 'c')) == 'CONCAT("a", "b", "c")'


def test_factory():
    fn = _fn_factory('TESTFUNC')
    assert str(fn(1, 'a', Column('b').AS('colb'), '2')) == 'TESTFUNC(1,a,b,2)'
