from .parts import Column


def BETWEEN(expr1, expr2, expr3):
    return Column('%s BETWEEN %s AND %s' % (_actual_n(expr1), _actual_n(expr2), _actual_n(expr3)))


def CAST(type1, type2):
    return Column('CAST(%s AS %s)' % (type1, type2))


def CONCAT(*args):
    arg = [_actual_n(a) for a in args]
    arg = ', '.join(arg)
    return Column('CONCAT(%s)' % arg)


def CONTAINS(exp, search_str):
    return Column('%s CONTAINS %s' % (_actual_n(exp), _actual_n(search_str)))


def IN(search_expr, *expr):
    return Column('%s IN(%s)' % (_actual_n(search_expr), ', '.join(_actual_n(x) for x in expr)))


def IS_NULL(expr):
    return Column('%s IS NULL' % _actual_n(expr))


def _fn_factory(name):
    def _fn(*col):
        return Column('{0}({1})'.format(name, ','.join(_actual_n(x) for x in col)))
    return _fn


def _actual_n(col):
    if isinstance(col, str):
        return "'%s'" % col
    elif isinstance(col, Column):
        return str(col.real_name)
    else:
        return str(col)
