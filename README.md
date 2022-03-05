 # Task: Calculate a running cumulative total

An sqlite database is stored in the same directory as this notebook called `orders.db`. The names of the tables and their columns are provided below. Your task is to calculate a cumulative running total for each customer's purchases. 


**For example...if I have the following table:**

|  person  |  date | amount_spent |
|:--------:|:-----:|:------------:|
| person 1 | day 1 |       1      |
| person 2 | day 1 |       5      |
| person 1 | day 2 |       2      |
| person 2 | day 2 |       8      |
| person 1 | day 3 |       9      |
| person 2 | day 3 |       2      |


**A cumulative total for the above table would produce the following table:**


|  person  |  date | cumulative_total |
|:--------:|:-----:|:------------:|
| person 1 | day 1 |       1      |
| person 2 | day 1 |       5      |
| person 1 | day 2 |       3      |
| person 2 | day 2 |       13     |
| person 1 | day 3 |       12     |
| person 2 | day 3 |       15     |


## SQL Tables

### Table name: `orders`

**Columns:**
- `order_id`
- `amount_spent`

### Table name: `customer_activity`

**Columns:**
- `date`
- `customer_id`
- `order_id`

**Some starter code has been provided to set up a connection to the database and make querying the database easier...**

Below, I define a helper function to make it easy for you to write your query. 


```python
# Run this code unchanged
import pandas as pd
import sqlite3
conn = sqlite3.connect('orders.db')

def run_query(query_string):
    
    return pd.read_sql(query_string, conn)
```

**Here is an example of writing an sql query in a jupyter notebook...**


```python
# Run this code unchanged

## Triple quotations are used
## to allow for a multiline string
query = """

select *
from example_table
order by col3 desc

"""

## Pass the query into the `run_query` function
run_query(query)
```

# Write your query

Your query should produce a table with the following columns
- date
- customer_id
- cumulative_total

**Sort the results by `date` in ascending order**


```python
# YOUR CODE GOES HERE

query = """




"""
```


```python
# Inspect the output of your query here
run_query(query)
```


```python
# Run this code to test the results of your query
from tests import test
a, r = test(query)
```
