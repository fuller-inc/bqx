class Comparable:
    """Abstract class of 'comparable' clauses.

    Please mind that 'comparable' is not about Python, but is about SQL.
    Inherit this to clarify that sub-classes can't be 'calculated' without explicit implementation.
    See implementations in parts.py.
    """
    def __init__(self):
        pass

    def __lt__(self, other):
        # self < other
        raise NotImplementedError

    def __le__(self, other):
        # self <= other
        raise NotImplementedError

    def __eq__(self, other):
        # self == other
        raise NotImplementedError

    def __ne__(self, other):
        # self != other
        raise NotImplementedError

    def __gt__(self, other):
        # self > other
        raise NotImplementedError

    def __ge__(self, other):
        # self >= other
        raise NotImplementedError


class Alias:
    """Subclass of Alias will be an alias of something like column and table.

    In SQL query like "column AS col", 'col' is an alias of 'column'.
    """
    def __init__(self, real_name):
        self.real_name = real_name
        self.alias_name = None

    def __str__(self):
        """Sub-classes have to define how this class looks like."""
        raise NotImplementedError

    def AS(self, alias):
        """Set alias name, declared in AS claus.

        Args:
            alias (str): Alias name

        Returns:
            self
        """
        self.alias_name = alias
        return self

    def as_claus(self):
        """Expand its real/alias name in AS claus form."""
        if self.alias_name:
            return '%s AS %s' % (self.real_name, self.alias_name)
        else:
            return self.real_name

    def alias_name(self):
        return self._alias_name

    def real_name(self):
        return self.real_name
