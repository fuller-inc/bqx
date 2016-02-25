from .parts import Column


def CAST(type1, type2):
    return Column('CAST(%s)' % _actual_n('%s AS %s' % (type1, type2)))

def CONCAT(*args):
    arg = ['"%s"' % _actual_n(a) for a in args]
    arg = ', '.join(arg)
    return Column('CONCAT(%s)' % arg)

def _fn_factory(name):
    def _fn(*col):
        return Column('{0}({1})'.format(name, ','.join(_actual_n(x) for x in col)))
    return _fn

def _actual_n(col):
    if isinstance(col, str):
        return col
    elif isinstance(col, Column):
        return col.real_name
    else:
        return str(col)

COUNT = _fn_factory('COUNT')
SUM = _fn_factory('SUM')
INTEGER = _fn_factory('INTEGER')
SQRT = _fn_factory('SQRT')
IF = _fn_factory('IF')
POW = _fn_factory('POW')
LEFT = _fn_factory('LEFT')
RIGHT = _fn_factory('RIGHT')
FORMAT_UTC_USEC = _fn_factory('FORMAT_UTC_USEC')
