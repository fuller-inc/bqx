BQX
===

*Author: Takumi Sueda*

Generage sophisticated query in simple way.

What's this?
------------

This library is focused to generate queries for Google BigQuery. It's
similar to SQLAlchemy, but BQX acts just as a querygenerator so I
suggest you to use this with front-ends like pandas, along with Jupyter
Notebook. (See 'example' folder for demonstrations of BQX w/ pandas and
Jupyter Notebook.)

Example
-------

::

    >>> from bqx.query import Query as Q
    >>> from bqx.parts import Table as T, Column as C
    >>> from bqx.func import SUM
    >>>
    >>> shakespeare = T('publicdata:samples.shakespeare')
    >>> word = C('word')
    >>> q = Q().SELECT(word).FROM(shakespeare).LIMIT(10)
    >>> print(q.getq())
    SELECT word
    FROM publicdata:samples.shakespeare
    LIMIT 10

    >>> count = C('word_count')
    >>> corpus = C('corpus')
    >>> count_sum = SUM(count).AS('count_sum')
    >>> q = (
    ...     Q()
    ...     .SELECT(corpus, count_sum)
    ...     .FROM(shakespeare)
    ...     .GROUP_BY(corpus)
    ...     .ORDER_BY(count_sum).DESC())
    >>> print(q.getq())
    SELECT corpus, SUM(word_count) AS count_sum
    FROM publicdata:samples.shakespeare
    GROUP BY corpus
    ORDER BY count_sum
    DESC

Why some functions are UPPERCASE?
---------------------------------

Yes, I know, UPPERCASE functions are not cool and discouraged to use.
Why I adopted them is to avoid collision with Python's reserved words.

The second reason is for SQL's UPPERCASE manners.
