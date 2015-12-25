from .parts import Column


def CAST(type1, type2):
    return Column('CAST(%s)' % _actual_n('%s AS %s' % (type1, type2)))

def CONCAT(*args):
    arg = ['"%s"' % _actual_n(a) for a in args]
    arg = ', '.join(arg)
    return Column('CONCAT(%s)' % arg)

def IF(cond, val_t, val_f):
    cond, val_t, val_f = (_actual_n(x) for x in [cond, val_t, val_f])
    return Column('IF(%s, %s, %s)' % (cond, val_t, val_f))

def _fn_factory(name):
    return lambda col: Column('{0}({1})'.format(name, _actual_n(col)))
    #return eval("lambda col: Column('{0}(%s)' % _actual_n(col))".format(name))

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