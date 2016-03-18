"""
Test of bqx.func.

Run Test: `tox` or `python setup.py test`
"""

from bqx.parts import Column
from bqx.func import *
from bqx.func import _fn_factory


funcs = ['COUNT', 'SUM', 'INTEGER', 'SQRT', 'IF', 'POW']
column = Column('column').AS('col')


def test_between():
    assert str(BETWEEN(column, 1, 10)) == 'column BETWEEN 1 AND 10'


def test_cast():
    assert str(CAST('type1', 'type2')) == 'CAST(type1 AS type2)'


def test_concat():
    assert str(CONCAT('a', 'b', 'c')) == "CONCAT('a', 'b', 'c')"


def test_contains():
    assert str(CONTAINS(column, 'miku')) == "column CONTAINS 'miku'"


def test_in():
    assert str(IN(column, 1, 2, 3)) == 'column IN(1, 2, 3)'


def test_is_null():
    assert str(IS_NULL(column)) == 'column IS NULL'


def test_factory():
    fn = _fn_factory('TESTFUNC')
    assert str(fn(1, 'a', Column('b').AS('colb'), '2')) == "TESTFUNC(1,'a',b,'2')"
