"""
Test of bqx.abstract.

Run Test: `tox` or `python setup.py test`
"""

from bqx.abstract import Alias


def test_auto_alias():
    a_manual = Alias('real.alias').AS('alias')
    a_auto = Alias('real.alias')

    assert a_manual.as_claus() == 'real.alias AS alias'
    assert a_auto.as_claus(auto_alias=False) == 'real.alias'
    assert a_auto.as_claus(auto_alias=True) == 'real.alias AS alias'
