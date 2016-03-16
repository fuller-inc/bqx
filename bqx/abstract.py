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

    def __add__(self, other):
        # self + other
        raise NotImplementedError

    def __sub__(self, other):
        # self - other
        raise NotImplementedError

    def __mul__(self, other):
        # self * other
        raise NotImplementedError

    def __truediv__(self, other):
        # self / other
        raise NotImplementedError

    def __mod__(self, other):
        # self % other
        raise NotImplementedError

    def __and__(self, other):
        # self & other
        raise NotImplementedError

    def __or__(self, other):
        # self | other
        raise NotImplementedError


class Alias:
    """Subclass of Alias will be an alias of something like column and table.

    In SQL query like "column AS col", 'column' is real name and 'col' is alias name.
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

    def as_claus(self, auto_alias=False):
        """Expand its real/alias name in AS claus form.

        If the alias name is not defined, auto-generated AS claus form
        or just real name will be returned. Behavior depends on auto_alias.

        Keyword Args:
            auto_alias (bool): Generate AS claus automatically or not

        Returns:
            str: Appropriate representation of alias object
        """
        if self.alias_name:
            return '%s AS %s' % (self.real_name, self.alias_name)
        else:
            if auto_alias and '.' in self.real_name:
                self.alias_name = self.real_name.split('.')[-1]
                return self.as_claus()
            else:
                return self.real_name

