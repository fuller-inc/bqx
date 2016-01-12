import textwrap
import bqx.parts
import bqx.abstract
from copy import deepcopy

Column = bqx.parts.Column
Table = bqx.parts.Table
Alias = bqx.abstract.Alias


class Query:
    def __init__(self, udf=[], indent=True):
        self.partial = True
        self.applied_c = []
        self.alias_name = None
        self.udf_funcs = udf
        self.indent = indent
        self.selected = False

    def __getattr__(self, item):
        if self.alias_name:
            return Column('%s.%s' % (self.alias_name, str(item)))
        else:
            raise Exception("Attribute/Function %s is not found. Call AS or register UDF funcs." % item)

    def __deepcopy__(self, memo):
        copied = type(self)()
        for k, v in self.__dict__.items():
            setattr(copied, k, deepcopy(v, memo))
        return copied

    def SELECT(self, *args, **kwargs):
        if self.selected:
            self.selected = False
            q = self.SELECT(*args, **kwargs)
            q = q.FROM(self)
            q.applied_c = q.applied_c[-2:]
            return q
        else:
            self.selected = True

        col = []
        for arg in args:
            if isinstance(arg, str):
                col.append(arg)
            elif isinstance(arg, Column) or isinstance(arg, Case):
                col.append(arg.as_claus())
            elif arg == self._Special.ALL:
                col.append('*')
        col += [Column(real).AS(alias).as_claus() for alias, real in kwargs.items()]
        return self._apply('SELECT %s' % ', '.join(col))

    def FROM(self, arg):
        t = self._as_claus(arg)
        if self.indent:
            t = textwrap.indent(t, '  ').lstrip()
        return self._apply('FROM %s' % t)

    def WHERE(self, cond):
        if self._is_next_to('FROM'):
            return self._apply('WHERE %s' % cond)
        else:
            raise Exception('WHERE clause is put in wrong place.')

    def ON(self, cond):
        if self._is_next_to('JOIN'):
            return self._apply('ON %s' % cond)
        else:
            raise Exception('ON clause is put in wrong place. Last clause: %s' % self.applied_c[-1])

    def ORDER_BY(self, row, desc=False):
        if desc:
            s = 'ORDER BY %s DESC' % str(row)
        else:
            s = 'ORDER BY %s' % str(row)
        return self._apply(s)

    def ASC(self):
        return self._add_decorator('ORDER BY', 'ASC')

    def DESC(self):
        return self._add_decorator('ORDER BY', 'DESC')

    def GROUP_BY(self, *rows):
        return self._apply('GROUP BY %s' % ', '.join([str(x) for x in rows]))

    def _JOIN(self, type, table):
        t = self._as_claus(table)
        return self._apply('%s JOIN %s' % (type, t))

    def INNER_JOIN(self, table):
        return self._JOIN('INNER', table)

    def LEFT_JOIN(self, table):
        return self._JOIN('LEFT', table)

    def EACH(self):
        if self._is_next_to('JOIN'):
            q = self.applied_c[-1].replace('JOIN', 'JOIN EACH')
            return self._replace(-1, q)
        elif self._is_next_to('GROUP BY'):
            q = self.applied_c[-1].replace('GROUP', 'GROUP EACH')
            return self._replace(-1, q)
        else:
            raise Exception('Not allowed to place EACH here.')

    def UDF(self, func):
        if func in self.udf_funcs:
            last_q = self.applied_c[-1]
            if last_q.startswith('FROM '):
                last_q = last_q[5:].strip('()')
                func_name = func.upper()
                s = 'FROM %s(%s)' % (func_name, last_q)
                return self._replace(-1, s)
            else:
                raise Exception("Can't apply func other than FROM clause.")
        else:
            raise Exception('%s is not registered as an UDF.' % func)

    def LIMIT(self, limit):
        return self._apply('LIMIT %d' % limit)

    def AS(self, alias_name):
        self.alias_name = alias_name
        return self

    def getq(self, end='\n', bracket=False):
        if bracket:
            s = '(%s)'
        else:
            s = '%s'
        return s % end.join(self.applied_c)

    def _apply(self, clause):
        newself = deepcopy(self)
        newself.applied_c.append(clause)
        return newself

    def _replace(self, index, new_clause):
        newself = deepcopy(self)
        newself.applied_c[index] = new_clause
        return newself

    def _is_next_to(self, last_claus):
        if self.applied_c[-1].find(last_claus) >= 0:
            return True
        else:
            return False

    def _as_claus(self, arg):
        if isinstance(arg, Table):
            t = arg.as_claus()
        elif isinstance(arg, Query):
            t = '(%s)' % arg.getq()
            if arg.alias_name:
                t = '%s AS %s' % (t, arg.alias_name)
        else:
            t = arg
        return t

    def _add_decorator(self, last_clause, deco):
        if self._is_next_to(last_clause):
            return self._apply(deco)
        else:
            raise Exception("Can't add decorator %s here." % deco)


class Case(Alias):
    def __init__(self):
        super().__init__(self)
        self.conds = []

    def __str__(self):
        if self.alias_name:
            return self.alias_name
        else:
            return self.real_name

    def WHEN(self, cond):
        self.conds.append([cond, 0])
        return self

    def THEN(self, val):
        self.conds[-1][1] = val
        return self

    def END(self):
        template = '\nCASE %s\nEND'
        conds_str = ['WHEN {cond} THEN {val}'.format(cond=c[0], val=repr(str(c[1]))) for c in self.conds]
        self.real_name = template % '\n'.join(conds_str)
        return self
