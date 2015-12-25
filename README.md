BQX
=====
*Author: Takumi Sueda*

Generage sophisticated query in simple way.


## What's this?
This library is focused to generate (literally) big query for Google BigQuery.
It's similar to SQLAlchemy but simpler and easy to learn.

Features on which I focused are:

 - UPPERCASE syntax that is similar to SQL (and dialects.)
 - Easy to use for non-programmers like data analysts.


## Why some functions are UPPERCASE?
Yes, I know, UPPERCASE functions are not cool and discouraged to use.
Why I adopted them is because I don't like SQLAlchemy's naming rule;
`select` and `where` are straightforward for example, but how about `as_` ?

I think it's painful to put underscores next to reserved words in Python,
while other words don't have decorations...

One day, I was talking with co-worker about SQL and BigQuery. He likes to
write SQL query in mixed-case style like `FROM foo SELECT bar WHERE blahblah`.
I asked him why, and he replied; it's easy to read rather than
`from foo select bar where blahblah` because it's easy to identify whether
a word is SQL-related or not.

For these backgrounds, I chose UPPERCASE for BQX finally.