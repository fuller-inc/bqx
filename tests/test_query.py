"""
Test of bqx.query.
Commented-out assert lines indicates it's not implemented yet.

Run Test: `tox` or `python setup.py test`
"""

import pytest
from bqx.query import Query as Q, Case as CASE
from bqx.parts import Column as C, Table as T

# Test with basic str argument for simplicity
column = 'column'
column_obj = C('column').AS('col')
column_foo = C('column').AS('foo')
column_bar = C('column').AS('bar')
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
    try:
        Q().column  # Get attribute without setting alias name
    except Exception:
        pytest.fail("Unexpected exception raised")

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
    joins = [('Q().INNER_JOIN', 'INNER JOIN'), ('Q().LEFT_OUTER_JOIN', 'LEFT OUTER JOIN'), ('Q().CROSS_JOIN', 'CROSS JOIN')]
    for fn, name in joins:
        assert eval(fn)(table).getq() == '%s table' % name
        assert eval(fn)(table_obj).getq() == '%s table AS tbl' % name
        assert eval(fn)(table_obj).EACH().getq() == '%s EACH table AS tbl' % name
        assert eval(fn)(table_obj).ON(column_obj == 'foo').getq() == "%s table AS tbl\nON col = 'foo'" % name
        assert eval(fn)(table_obj).EACH().ON(column_obj == 'foo').getq() == "%s EACH table AS tbl\nON col = 'foo'" % name

    with pytest.raises(Exception):
        q.ON('cond')  # Call ON without calling JOINs


def test_group_by():
    assert Q().GROUP_BY(column).getq() == 'GROUP BY column'
    assert Q().GROUP_BY(column_obj).getq() == 'GROUP BY col'
    assert Q().GROUP_BY(column_obj).EACH().getq() == 'GROUP EACH BY col'


def test_where():
    q = Q().SELECT(column_obj).FROM(table_obj)
    assert q.WHERE('col = 1234').getq() == 'SELECT column AS col\nFROM table AS tbl\nWHERE col = 1234'
    assert q.WHERE(column_obj == 1234).getq() == 'SELECT column AS col\nFROM table AS tbl\nWHERE col = 1234'


def test_having():
    q = Q().SELECT(column_obj).FROM(table_obj)
    assert q.HAVING('col = 1234').getq() == 'SELECT column AS col\nFROM table AS tbl\nHAVING col = 1234'
    assert q.HAVING(column_obj == 1234).getq() == 'SELECT column AS col\nFROM table AS tbl\nHAVING col = 1234'


def test_on():
    ideal = 'SELECT column AS col\nFROM table AS tbl\nINNER JOIN table_foo AS foo\nON tbl.x = foo.x'
    q = Q().SELECT(column_obj).FROM(table_obj).INNER_JOIN(table_foo)
    assert q.ON('tbl.x = foo.x').getq() == ideal
    assert q.ON(table_obj.x == table_foo.x).getq() == ideal


def test_omit_record_if():
    ideal = 'SELECT column AS col\nFROM table AS tbl\nOMIT RECORD IF col = 1234'
    q = Q().SELECT(column_obj).FROM(table_obj)
    assert q.OMIT_RECORD_IF('col = 1234').getq() == ideal
    assert q.OMIT_RECORD_IF(column_obj == 1234).getq() == ideal


def test_order_by():
    for col_name, alias_name in [(column, 'column'), (column_obj, 'col')]:
        assert Q().ORDER_BY(col_name).getq() == 'ORDER BY %s' % alias_name
        assert Q().ORDER_BY(col_name).ASC().getq() == 'ORDER BY %s\nASC' % alias_name
        assert Q().ORDER_BY(col_name).DESC().getq() == 'ORDER BY %s\nDESC' % alias_name
        for another_col in [column_foo, 'foo']:
            assert Q().ORDER_BY(another_col, col_name).DESC(another_col).getq() == 'ORDER BY foo DESC, %s' % alias_name

    with pytest.raises(Exception):
        Q().ASC()  # Call ASC (and other decorators) in wrong place


def test_limit():
    assert Q().LIMIT(3939).getq() == 'LIMIT 3939'


def test_each():
    assert Q().INNER_JOIN(table_obj).EACH().getq() == 'INNER JOIN EACH table AS tbl'
    assert Q().GROUP_BY(column_obj).getq() == 'GROUP BY col'

    with pytest.raises(Exception):
        Q().EACH()  # Call EACH without calling JOINs or GROUP BY


def test_case():
    assert Q().SELECT(case).getq() == "SELECT \nCASE WHEN col = 'miku' THEN 'wow'\nEND"

    with pytest.raises(NotImplementedError):
        str(CASE())  # CASE supports neither conversion nor aliasing.


def test_select_chain():
    q = (
        Q()
        .SELECT(column_obj)
        .FROM(table_obj).AS('foo')
        .SELECT('col')
        .ORDER_BY(column_obj))

    assert q.getq() == 'SELECT col\nFROM (SELECT column AS col\n  FROM table AS tbl) AS foo\nORDER BY col'


def test_join_chain():
    q = (
        Q()
        .SELECT(table_obj.x, table_foo.y, table_bar.z)
        .FROM(table_obj)
        .INNER_JOIN(table_foo)
        .ON(table_obj.x == table_foo.x)

        .INNER_JOIN(table_bar)
        .ON(table_obj.x == table_bar.x))

    # assert q.getq() == 'SELECT tbl.x, foo.y, bar.z\nFROM (SELECT *\n  FROM table AS tbl\n  INNER JOIN table_foo AS foo\n  ON tbl.x = foo.x)\nINNER JOIN table_bar AS bar\nON tbl.x = bar.x'


def test_udf():
    q = Q(udf=['func'])
    assert q.FROM(table_obj).UDF('func').getq() == 'FROM FUNC(table AS tbl)'

    with pytest.raises(Exception):
        q.UDF('func')  # Call UDF in wrong place

    with pytest.raises(Exception):
        q.FROM(table_obj).UDF('unknown_func')  # Call UDF without defining UDFs in constructor
