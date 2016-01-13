"""
Test of bqx.query.
Commented-out assert lines indicates it's not implemented yet.

Run Test: `py.test` or `python -m pytest`
"""

import pytest
from bqx.query import Query as Q, Case as CASE
from bqx.parts import Column as C, Table as T

# Test with basic str argument for simplicity
column = 'column'
column_obj = C('column').AS('col')
table = 'table'
table_obj = T('table').AS('tbl')
table_foo = T('table_foo').AS('foo')
table_bar = T('table_bar').AS('bar')
nested_q = Q().SELECT('*').FROM('table').AS('nested')
nested_q_str = nested_q.getq()
node = 'node'

case = CASE().WHEN(column_obj == 'miku').THEN('wow').END()
# flatten = FLATTEN(table_foo, column_obj)
# flatten_nested = FLATTEN(nested_q, column_obj)


def test_creation():
    # Blank
    assert Q().getq() == ''
    # SELECT for test
    assert Q().SELECT('column').FROM('table').getq() == 'SELECT column\nFROM table'
    assert Q().SELECT('column').FROM('table').getq(end=' ') == 'SELECT column FROM table'


def test_accessing_attributes():
    with pytest.raises(Exception):  # Get attribute without setting alias name
        Q().column
    assert str(Q().AS('alias_name').column) == 'alias_name.column'  # Get attribute after setting alias name


def test_select():
    assert Q().SELECT(column).getq() == 'SELECT column'
    assert Q().SELECT(column_obj).getq() == 'SELECT column AS col'


def test_within():
    pass
    # assert Q().SELECT(column).WITHIN(node).getq() == 'SELECT column WITHIN node'
    # assert Q().SELECT(column).WITHIN_RECORD().getq() == 'SELECT column WITHIN RECORD'
    # assert Q().SELECT(column_obj).WITHIN(node).getq() == 'SELECT column WITHIN node AS col'
    # assert Q().SELECT(column_obj).WITHIN_RECORD().getq() == 'SELECT column WITHIN RECORD AS col'


def test_from():
    assert Q().FROM(table).getq() == 'FROM table'
    assert Q().FROM(table_obj).getq() == 'FROM table AS tbl'

    # Union
    # assert Q().FROM(table_obj, table_obj).getq() == 'FROM table AS tbl, table AS tbl'

    # Nested
    assert Q().FROM(nested_q).getq() == 'FROM (SELECT *\n  FROM table) AS nested'
    assert Q(indent=False).FROM(nested_q).getq() == 'FROM (SELECT *\nFROM table) AS nested'


def test_flatten():
    pass
    # assert Q().FROM(flatten).getq() == 'FROM FLATTEN(table_foo, column)'
    # assert Q().FROM(flatten_nested).getq() == 'FROM FLATTEN(SELECT *\n  FROM table, column)'


def test_join():
    q = Q()
    joins = [(q.INNER_JOIN, 'INNER JOIN'), (q.LEFT_OUTER_JOIN, 'LEFT OUTER JOIN'), (q.CROSS_JOIN, 'CROSS JOIN')]
    for fn, name in joins:
        assert fn(table).getq() == '%s table' % name
        assert fn(table_obj).getq() == '%s table AS tbl' % name
        assert fn(table_obj).EACH().getq() == '%s EACH table AS tbl' % name
        assert fn(table_obj).ON(column_obj == 'foo').getq() == "%s table AS tbl\nON col = 'foo'" % name
        assert fn(table_obj).EACH().ON(column_obj == 'foo').getq() == "%s EACH table AS tbl\nON col = 'foo'" % name


def test_where():
    q = Q().SELECT(column_obj).FROM(table_obj)
    assert q.WHERE('col = 1234').getq() == 'SELECT column AS col\nFROM table AS tbl\nWHERE col = 1234'
    assert q.WHERE(column_obj == 1234).getq() == 'SELECT column AS col\nFROM table AS tbl\nWHERE col = 1234'

    with pytest.raises(Exception):
        Q().WHERE('cond')


def test_group_by():
    assert Q().GROUP_BY(column).getq() == 'GROUP BY column'
    assert Q().GROUP_BY(column_obj).getq() == 'GROUP BY col'
    assert Q().GROUP_BY(column_obj).EACH().getq() == 'GROUP EACH BY col'


def test_having():
    q = Q().SELECT(column_obj).FROM(table_obj)
    # assert q.HAVING('col = 1234').getq() == 'SELECT column\nFROM table AS tbl\nHAVING col = 1234'
    # assert q.HAVING(column_obj == 1234).getq() == 'SELECT column\nFROM table AS tbl\nHAVING col = 1234'


def test_order_by():
    assert Q().ORDER_BY(column).ASC().getq() == 'ORDER BY column\nASC'
    assert Q().ORDER_BY(column).DESC().getq() == 'ORDER BY column\nDESC'

    assert Q().ORDER_BY(column_obj).ASC().getq() == 'ORDER BY col\nASC'
    assert Q().ORDER_BY(column_obj).DESC().getq() == 'ORDER BY col\nDESC'


def test_limit():
    assert Q().LIMIT(3939).getq() == 'LIMIT 3939'


def test_case():
    assert Q().SELECT(case).getq() == "SELECT \nCASE WHEN col = 'miku' THEN 'wow'\nEND"


def test_select_chain():
    q = (
        Q()
        .SELECT(column_obj)
        .FROM(table_obj)
        .SELECT('col')
        .ORDER_BY(column_obj))

    assert q.getq() == 'SELECT col\nFROM (SELECT column AS col\n  FROM table AS tbl)\nORDER BY col'