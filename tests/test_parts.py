"""
Test of bqx.parts.

Run Test: `tox` or `python setup.py test`
"""

import pytest
from bqx.parts import Table, Column, Flatten


table = Table('table')
table_as = Table('table').AS('tbl')
flatten = Flatten('table', 'nested_tablelike')
flatten_cplx = Flatten(table_as, table_as.col)
column = Column('column')
column_as = Column('column').AS('col')


def test_table():
    try:
        table.column  # Access column without defining alias
    except Exception:
        pytest.fail("Unexpected exception raised")

    assert str(table_as) == 'tbl'
    assert str(table_as.column) == 'tbl.column'


def test_flatten():
    assert str(flatten) == 'FLATTEN(table, nested_tablelike)'
    assert str(flatten_cplx) == 'FLATTEN(table, col)'


def test_column():
    ops = [
        (column_as.__lt__, '<'),
        (column_as.__le__, '<='),
        (column_as.__eq__, '='),
        (column_as.__ne__, '!='),
        (column_as.__gt__, '>'),
        (column_as.__ge__, '>='),
        (column_as.__add__, '+'),
        (column_as.__sub__, '-'),
        (column_as.__mul__, '*'),
        (column_as.__truediv__, '/'),
        (column_as.__mod__, '%'),
        (column_as.__and__, '&'),
        (column_as.__or__, '|'),
    ]

    for op, rep in ops:
        assert op(column_as) == 'col %s col' % rep
        assert op(column) == 'col %s column' % rep

    assert column_as.__eq__(None) == 'col IS NULL'


def test_complex_calc():
    assert str(column_as + column_as + column_as + column_as) == '(((col + col) + col) + col)'
    assert str(column_as + column_as - column_as * column_as / column_as) == '((col + col) - ((col * col) / col))'
    assert str(column_as / (column_as * 39)) == '(col / (col * 39))'
    assert str((column_as == 5) & (column_as >= 39)) == '(col = 5) AND (col >= 39)'
    assert str((column_as == 5) | (column_as >= 39)) == '(col = 5) OR (col >= 39)'
