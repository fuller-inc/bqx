import textwrap
import bqx.parts
import bqx.abstract
import os
import hashlib
from copy import deepcopy

Column = bqx.parts.Column
Table = bqx.parts.Table
Alias = bqx.abstract.Alias


class Query:
    def __init__(self, udf=[], indent=True, auto_alias=False):
        self.partial = True
        self.applied_c = []
        self.alias_name = None
        self.udf_funcs = udf
        self.indent = indent
        self.auto_alias = auto_alias
        self.selected = False  # Flag for SELECT chain
        self.joined = False  # Flag for JOIN chain

        # Alternative alias used if necessary (e.g. alias name is not defined by user)
        self.alias_name_rnd = self.gen_random_alias()

    def __getattr__(self, item):
        if self.alias_name:
            alias = self.alias_name
        else:
            # Alias is not defined. Use auto-generated alias name.
            alias = self.alias_name_rnd
        return Column('%s.%s' % (alias, str(item)))

    def __deepcopy__(self, memo):
        copied = type(self)()
        for k, v in self.__dict__.items():
            setattr(copied, k, deepcopy(v, memo))
        return copied

    def SELECT(self, *columns):
        if self.selected:
            self.selected = False
            q = self.SELECT(*columns)
            q = q.FROM(self)
            q.applied_c = q.applied_c[-2:]
            return q
        else:
            self.selected = True

        col = []
        for arg in columns:
            if isinstance(arg, str):
                col.append(arg)
            elif isinstance(arg, Column) or isinstance(arg, Case):
                col.append(arg.as_claus(auto_alias=self.auto_alias))
        # col += [Column(real).AS(alias).as_claus() for alias, real in kwargs.items()]
        return self._apply('SELECT %s' % ', '.join(col))

    def FROM(self, *tables):
        tbl = []
        for t in tables:
            if isinstance(t, str):
                tbl.append(t)
            else:
                tbl.append(t.as_claus())
        if self.indent:
            t = textwrap.indent(', '.join(tbl), '  ').lstrip()
        else:
            t = ', '.join(tbl)
        return self._apply('FROM %s' % t)

    def WHERE(self, cond):
        return self._apply('WHERE %s' % cond)

    def HAVING(self, cond):
        return self._apply('HAVING %s' % cond)

    def ON(self, cond):
        if self._is_next_to('JOIN'):
            return self._apply('ON %s' % cond)
        else:
            raise Exception('ON clause is put in wrong place. Last clause: %s' % self.applied_c[-1])

    def OMIT_RECORD_IF(self, cond):
        return self._apply('OMIT RECORD IF %s' % cond)

    def ORDER_BY(self, *columns):
        s = 'ORDER BY %s' % ', '.join(str(x) for x in columns)
        return self._apply(s)

    def ASC(self):
        return self._add_decorator('ORDER BY', 'ASC')

    def DESC(self, *columns):
        if len(columns) == 0:
            return self._add_decorator('ORDER BY', 'DESC')
        newself = deepcopy(self)
        for _col in columns:
            col = str(_col)
            newself = newself._replace_partly(-1, col, col + ' DESC')
        return newself

    def GROUP_BY(self, *rows):
        return self._apply('GROUP BY %s' % ', '.join([str(x) for x in rows]))

    def _JOIN(self, type, table):
        if self.joined:
            self.joined = False
            self.selected = False
            newq_outer = deepcopy(self)
            newq_outer.applied_c = newq_outer.applied_c[:1]

            c = deepcopy(self.applied_c)[1:]
            self.applied_c = []
            newq_inner = self.SELECT('*')
            newq_inner.applied_c.extend(c)

            newq_outer = newq_outer.FROM(newq_inner)
            newq_outer = newq_outer._JOIN(type, table)
            return newq_outer
        else:
            self.joined = True

        if isinstance(table, str):
            t = table
        else:
            t = table.as_claus()
        return self._apply('%s JOIN %s' % (type, t))

    def INNER_JOIN(self, table):
        return self._JOIN('INNER', table)

    def FULL_OUTER_JOIN(self, table):
        return self._JOIN('FULL OUTER', table)

    def RIGHT_OUTER_JOIN(self, table):
        return self._JOIN('RIGHT OUTER', table)

    def LEFT_OUTER_JOIN(self, table):
        return self._JOIN('LEFT OUTER', table)

    def CROSS_JOIN(self, table):
        return self._JOIN('CROSS', table)

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
            if self._is_next_to('FROM'):
                last_q = self.applied_c[-1]
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

    def as_claus(self):
        if self.alias_name:
            alias = self.alias_name
        else:
            alias = self.alias_name_rnd
        return '%s AS %s' % (self.getq(bracket=True), alias)

    def gen_random_alias(self):
        return hashlib.md5(os.urandom(100)).hexdigest()[:7]

    def _apply(self, clause):
        newself = deepcopy(self)
        newself.applied_c.append(clause)
        return newself

    def _replace_partly(self, index, target_keyword, alt_keyword):
        if self.applied_c[index].find(target_keyword) == -1:
            raise ValueError("Keyword %s is not in original string %s ." % (target_keyword, self.applied_c[index]))
        newself = deepcopy(self)
        newself.applied_c[index] = newself.applied_c[index].replace(target_keyword, alt_keyword)
        return newself

    def _replace(self, index, new_clause):
        newself = deepcopy(self)
        newself.applied_c[index] = new_clause
        return newself

    def _is_next_to(self, last_claus):
        try:
            if self.applied_c[-1].find(last_claus) >= 0:
                return True
        except IndexError:
            pass
        return False

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
        raise NotImplementedError

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
