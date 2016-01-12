#####################################################
#This file is auto-generated from pandas_demo.ipynb.#
#####################################################

# # BQX Jupyter Notebook Demo
# 
# This example shows you how to play with data along with pandas.
# 
# Communication between this code and BigQuery API is fully automated thanks to pandas.

# ## Initialize

# In[1]:

from bqx.query import Query as Q
from bqx.parts import Table as T, Column as C
from bqx.func import SUM
import pandas as pd
import pandas.io.gbq as gbq


# ## Create query

# In[2]:

shakespeare = T('publicdata:samples.shakespeare')
count = C('word_count')
corpus = C('corpus')
count_sum = SUM(count).AS('count_sum')

q = (
    Q()
    .SELECT(corpus, count_sum)
    .FROM(shakespeare)
    .GROUP_BY(corpus)
    .ORDER_BY(count_sum).DESC())
print(q.getq())


# ## Execute query
# 
# Excecuting query and retrieving result are really easy. Just call pandas.io.gbq.read_gbq() with Query.getq() inside and you'll get a DataFrame.
# 
# That's it!

# In[6]:

gbq.read_gbq(q.getq(), 'YOUR_PROJECT_ID', reauth=True)

