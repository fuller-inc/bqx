import bqx.abstract

Alias = bqx.abstract.Alias
Comparable = bqx.abstract.Comparable


class Table(Alias):
    def __init__(self, real):
        if isinstance(real, str):
            super().__init__(real)

    def __getattr__(self, item):
        if self.alias_name == None:
            raise Exception('Define alias name using AS.')
        return Column('%s.%s' % (self.alias_name, item))

    def __str__(self):
        return self.alias_name


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

    def __and__(self, other):
        return self._cond_t('AND', other)

    def __or__(self, other):
        return self._cond_t('OR', other)

    def _cond_t(self, op, other):
        if self.alias_name:
            n = self.alias_name
        else:
            n = self.real_name

        if isinstance(other, str):
            other = repr(other)
        return Column('%s %s %s' % (n, op, str(other)))


class Func:
    def __init__(self, func_name, code):
        self.func_name = func_name
        self.code = code

    def __repr__(self):
        return self.expand()

    def __str__(self):
        return self.expand()

    def expand(self):
        return '%s(%s)' % (self.func_name, self.arg)