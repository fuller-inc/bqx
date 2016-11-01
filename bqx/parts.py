import os
import hashlib
import string
import random
import bqx.abstract

Alias = bqx.abstract.Alias
Comparable = bqx.abstract.Comparable


class Table(Alias):
    char_list = string.ascii_letters + string.digits

    def __init__(self, real):
        if isinstance(real, str):
            super().__init__(real)

    def __getattr__(self, item):
        if self.alias_name == None:
            self.alias_name = 'T%s' % ''.join(random.choice(self.char_list) for _ in range(4))
        return Column('%s.%s' % (self.alias_name, item))

    def __str__(self):
        return self.alias_name


class Flatten:
    def __init__(self, *table):
        self.tables = []

        for t in table:
            if isinstance(t, Column):
                self.tables.append(t.real_name.split('.')[-1])
            elif isinstance(t, Table):
                self.tables.append(t.real_name)
            elif isinstance(t, str):
                self.tables.append(t)

    def __str__(self):
        return 'FLATTEN(%s)' % ', '.join(self.tables)


class Column(Comparable, Alias):
    def __init__(self, real_name):
        """Initiate Column.

        Args:
            real_name (str): Its name which includes both table name and column name.

        Example:
            >>> alias = Column('table.column').AS('alias')
            >>> print(str(alias))
            'alias'
            >>> print(alias.real_name)
            'table.column'
        """
        Alias.__init__(self, real_name)

    def __getattr__(self, item):
        if item.startswith('__'):
            return None
        raise TypeError("Column doesn't have members.")

    def __str__(self):
        if self.alias_name:
            return self.alias_name
        else:
            return self.real_name

    def __lt__(self, other):
        return self._cond_t('<', other)

    def __le__(self, other):
        return self._cond_t('<=', other)

    def __eq__(self, other):
        return self._cond_t('=', other)

    def __ne__(self, other):
        return self._cond_t('!=', other)

    def __gt__(self, other):
        return self._cond_t('>', other)

    def __ge__(self, other):
        return self._cond_t('>=', other)

    def __add__(self, other):
        return self._cond_t('+', other)

    def __sub__(self, other):
        return self._cond_t('-', other)

    def __mul__(self, other):
        return self._cond_t('*', other)

    def __truediv__(self, other):
        return self._cond_t('/', other)

    def __mod__(self, other):
        return self._cond_t('%', other)

    def __and__(self, other):
        return self._cond_t('AND', other)

    def __or__(self, other):
        return self._cond_t('OR', other)

    def _cond_t(self, op, other):
        if self.alias_name:
            n = self.alias_name
        else:
            n = self.real_name

        if other is None:
            if op == '=':
                op = 'IS'
            elif op == '!=':
                op = 'IS NOT'
            t = '%s %s %s'
            other = 'NULL'
        else:
            if isinstance(other, str):
                other = repr(other)

            if op == 'AND' or op == 'OR':
                t = '(%s) %s %s'
            elif op != '=':
                t = '(%s %s %s)'
            else:
                t = '%s %s %s'

        return Column(t % (n, op, str(other)))
