BQX
=====
*Author: Takumi Sueda*

Generage sophisticated query for Google BigQuery in simple way.


### What is BQX?
BQX is a minimal query generator for Google BigQuery.
It's intended for being used by data analysts / scientists
who want to analyze big data.

BQX fires its power especially on making LONG and NESTED query.
BigQuery doesn't accept two or more queries at once so
user has to make views or make terribly nested query.
BQX's **sub query reference** feature and **SELECT chain** feature
helps you make long query. See samples for usage.


## How can I use it?
Running example on REPL is good for getting started,
and we suggest you to use BQX with front-ends like pandas for next step.
Communication between your code and BigQuery API is fully automated
thanks to pandas. Please take a look at 'pandas_demo.py' and
'pandas_demo.ipynb' for Jupyter Notebook.


## Is it only for BigQuery? How about MySQL or else?
It aims to generate query excecuted on BigQuery but it might be
applied to other SQL environments because
difference between plain SQL and BigQuery is small.

We are using some compute engines which can process SQL
(and dialects) like BigQuery, Hadoop and Spark.
So in near future, adding other SQL dialect is planned.


## Is it ORM?
No. It looks like ORM, but essentially it isn't.


## Is it ready to use?
Some important clauses are not implemented at present. 


## Why some functions are UPPERCASE?
The first reason is for avoiding collision with Python's reserved words.
The another reason is for SQL's UPPERCASE manners.


## Installing
    pip install bqx


## Example
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
