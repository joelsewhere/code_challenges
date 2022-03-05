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




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>col1</th>
      <th>col2</th>
      <th>col3</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>4</td>
      <td>5</td>
      <td>6</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1</td>
      <td>2</td>
      <td>3</td>
    </tr>
  </tbody>
</table>
</div>



# Write your query

Your query should produce a table with the following columns
- date
- customer_id
- cumulative_total

**Sort the results by `date` in ascending order**


```python

query = """

select date
     , customer_id
     , sum(amount_spent) 
       over(partition by customer_id 
            order by date 
            rows unbounded preceding) cumulative_total
from orders o
join customer_activity c
on o.order_id = c.order_id
order by date asc

"""
```


```python
# Inspect the output of your query here
run_query(query)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>date</th>
      <th>customer_id</th>
      <th>cumulative_total</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2021-05-09 20:36:10.930989</td>
      <td>d945201f-e671-4404-9ed7-8cd5930909a6</td>
      <td>2.052925</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2021-05-10 20:36:10.930989</td>
      <td>f1ef9d1e-75df-403f-ae2c-b3615248f3dc</td>
      <td>26.615839</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2021-05-11 20:36:10.930989</td>
      <td>a2d9c4c3-1081-4a9c-b9af-ac162a87ef64</td>
      <td>13.575465</td>
    </tr>
    <tr>
      <th>3</th>
      <td>2021-05-12 20:36:10.930989</td>
      <td>306bed34-5643-412d-9bf8-80c446774419</td>
      <td>3.836420</td>
    </tr>
    <tr>
      <th>4</th>
      <td>2021-05-13 20:36:10.930989</td>
      <td>ba2216d6-4cbc-471d-b62d-4128af46099e</td>
      <td>24.635933</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>295</th>
      <td>2022-02-28 20:36:10.930989</td>
      <td>d945201f-e671-4404-9ed7-8cd5930909a6</td>
      <td>403.691951</td>
    </tr>
    <tr>
      <th>296</th>
      <td>2022-03-01 20:36:10.930989</td>
      <td>d945201f-e671-4404-9ed7-8cd5930909a6</td>
      <td>421.599754</td>
    </tr>
    <tr>
      <th>297</th>
      <td>2022-03-02 20:36:10.930989</td>
      <td>f1ef9d1e-75df-403f-ae2c-b3615248f3dc</td>
      <td>781.334980</td>
    </tr>
    <tr>
      <th>298</th>
      <td>2022-03-03 20:36:10.930989</td>
      <td>ba2216d6-4cbc-471d-b62d-4128af46099e</td>
      <td>616.290965</td>
    </tr>
    <tr>
      <th>299</th>
      <td>2022-03-04 20:36:10.930989</td>
      <td>80809436-682c-4d5b-a1ea-c6b92b6142b4</td>
      <td>814.520910</td>
    </tr>
  </tbody>
</table>
<p>300 rows × 3 columns</p>
</div>




```python
# Run this code to test the results of your query
from tests import test
test(query)
```

    ✅ Correct!

