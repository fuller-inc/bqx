#####################################################
#This file is auto-generated from get_started.ipynb.#
#####################################################

# # Get Started
# 
# Here are some sample queries. See what BQX can do.

# ## Initialization

# In[1]:

from bqx.query import Query as Q
from bqx.parts import Table as T, Column as C
from bqx.func import SUM


# # 1. Simple examples

# ## 1.1 Make simple query.

# In[2]:

q = Q().SELECT('name').FROM('sample_table')
print(q.getq())


# ## 1.2 Get rid of quotes using Aliases.

# In[3]:

sample_table = T('sample_table')
name = C('name')

q = Q().SELECT(name).FROM(sample_table)
print(q.getq())


# ## 1.3 You'll want WHERE clause.
# 
# Column alias has overridden operators.  It provides syntax highlighting feature on conditions.

# In[4]:

sample_table = T('sample_table')
name = C('name')

q = Q().SELECT(name).FROM(sample_table).WHERE(name == 'Hatsune Miku')
print(q.getq())


# ## 1.4 SUM of column? Of course!

# In[5]:

sample_table = T('sample_table')
name = C('name')
score = C('score')
score_sum = SUM(score)

q = Q().SELECT(name, score_sum).FROM(sample_table).WHERE(name == 'Hatsune Miku').GROUP_BY(score)
print(q.getq())


# # 2. BQX's special features

# ## 2.1 Keep it partial. Use it later.
# 
# Put your query in in-complete state (we call it 'partial query'). Generate variety of queries with Python's power.

# In[6]:

sample_tables = [T('table_foo'), T('table_bar'), T('table_baz')]
name = C('name')

q = Q().SELECT(name)  # Query without FROM???

for table in sample_tables:
    print(q.FROM(table).getq())  # Now it's complete query
    print()


# ## 2.2 Escape from bracket hell.
# 
# I guess you have ever seen a nested query in nested query in nested query with bunch of AS clauses like:
# ``` sql
# SELECT average, name FROM (
#     SELECT pid, (a+b+c)/3 AS average, name FROM (
#         SELECT x.pid AS pid, x.a AS a, x.b AS b, x.c AS c, y.name AS name FROM [dataset.x] AS x INNER JOIN [dataset.y] as y ON x.pid = y.pid
#     )
# ) ORDER BY name
# ```
# 
# Here is a solution to this.
# 
# **Sub query reference** feature and **Auto alias** feature is used.

# In[7]:

# Call AS function manually to define AS clause.
x = T('table_x').AS('x')
y = T('table_y').AS('y')

# You don't have to call AS func all time.
# If you say auto_alias is True, AS clause will be auto-generated
# next to columns like 'x.pid', 'x.a', 'x.b', 'x.c' declared below.
q1 = (
    Q(auto_alias=True)
    .SELECT(x.pid, x.a, x.b, x.c, y.name)
    .FROM(x)
    .INNER_JOIN(y)
    .ON(x.pid == y.pid))

pid, name, a, b, c = C('pid'), C('name'), C('a'), C('b'), C('c')
average_calc = ((a + b + c) / 3).AS('average')

q2 = (
    Q()
    .SELECT(pid, average_calc, name)
    .FROM(q1))

average = C('average')

q3 = (
    Q()
    .SELECT(average, name)
    .FROM(q2)
    .ORDER_BY(name))

print(q3.getq())


# ## 2.3 I WANT MORE, MORE SIMPLE QUERY!!!
# 
# BQX have **SELECT chain** feature for simplification.
# Literally you *can* chain SELECT clauses and omit FROM clauses.
# 
# Here is another example which provides identical query shown above, with shorter code.

# In[8]:

x = T('table_x').AS('x')
y = T('table_y').AS('y')
pid, name, average, a, b, c = C('pid'), C('name'), C('average'), C('a'), C('b'), C('c')
average_calc = ((a + b + c) / 3).AS('average')

q = (
    Q(auto_alias=True)
    .SELECT(x.pid, x.a, x.b, x.c, y.name)
    .FROM(x)
    .INNER_JOIN(y)
    .ON(x.pid == y.pid)

    .SELECT(pid, average_calc, name)
    
    .SELECT(average, name)
    .ORDER_BY(name))

print(q.getq())

