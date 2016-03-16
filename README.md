BQX
=====
[![Build Status](https://img.shields.io/travis/fuller-inc/bqx/master.svg?style=flat-square)](https://travis-ci.org/fuller-inc/bqx)
[![Coverage Status](https://img.shields.io/coveralls/fuller-inc/bqx/master.svg?style=flat-square)](https://coveralls.io/github/fuller-inc/bqx?branch=master)

Generage sophisticated query for Google BigQuery in simple way.


## What is BQX?
BQX is a minimal query generator for Google BigQuery.
It's mainly intended for being used by data analysts / scientists
who want to analyze big data.

BQX fires its power especially on making LONG and NESTED query.
BigQuery doesn't accept two or more queries at once so
user has to make views or make terribly nested query.
BQX's features help you make long query preserving high readability.
See example for its features and usage.


## Requirements
 - Python 3.4 ~


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

See example directory for more detailed examples.


## License
This library is BSD-licensed.


## Q&A

### How can I use it?
Running example on REPL is good for getting started,
and we suggest you to use BQX with front-ends like pandas for next step.



### Is it only for BigQuery? How about MySQL or else?
It aims to generate query excecuted on BigQuery but it might be
applied to other SQL environments because
difference between plain SQL and BigQuery is small.

We are using some compute engines which can process SQL
(and dialects) like BigQuery, Hadoop and Spark.
So in near future, adding other SQL dialect is planned.


### Why some functions are UPPERCASE?
The first reason is for avoiding collision with Python's reserved words.
The another reason is for SQL's UPPERCASE manners.


### Is it ready to use?
We hope it's so.
All main clauses are implemented from v0.2.0, but not fully tested by hand yet.


### Where are documentations?
We're sorry but documentation is not available right now.
It will be published on ReadTheDocs.org soon. Stay tuned.
