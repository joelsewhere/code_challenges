## Task 1: Write an `SQL` query that counts how many sequential tasks a person has skipped. 

An sqlite3 database called `calculate_skips.db` is stored in this repository. This database contains a single table called `tasks`.

### Let's set up a connection to the database and load in the `tasks` table.

**Below we..**

- Open a connection to the sqlite database
- Define a helper function to make querying data easier


```python
#__CURRICULUM__
from tests import generate_test_data

generate_test_data(100)
```

    100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 100/100 [39:25<00:00, 23.66s/it]



```python
# Run this cell unchanged
import os
import sqlite3

# Open connection
db_path  = os.path.join('data', 'calculate_skips.db')
connection = sqlite3.connect(db_path)

# Helper function
def run_query(query_string):
    
    return pd.read_sql(query_string, connection)
```

To query the database you can pass a query string into the `run_query` helper function.


```python
# Run this cell unchanged
query = 'select * from tasks'

run_query(query)
```

### Write your query

Your query should return the following table:

| person | skipped |
|--------|:---------:|
|Person A| 1       |
|Person B| 2       |
|Person C| 0       |


```python
# Your code goes here
query = """


"""
```

**Run the cell below to check your query's result**


```python
# Run this cell unchanged
run_query(query)
```


```python
# Run this cell unchanged
from tests import test_query
test_query(query)
```

**Run the cell below to test your query**

## Task 2: Define a function that calculates skip counts in a pandas dataframe

Below, we load in the `tasks` table and store the data in the variable `df`


```python
# Run this cell unchanged
df = run_query('select * from tasks')
df.head(3)
```

In the cell below, define a function that
- Receives a dataframe with `['person', 'task_name', 'ordinality', 'completed']` columns
- Returns a table that counts the number of skipped lessons for each person

For the dataframe shown above, the function should output a table with the `person` column set as the index. The output should look like this:

| person | skipped |
|--------|:---------:|
|Person A| 1       |
|Person B| 2       |
|Person C| 0       |

_Please note: This function will be tested against *other* randomly generated datasets with the same column names and datatypes. So the function should be written to return skip counts for whatever dataset is passed as an argument_




```python
def calculate_skips(dataframe):
    # Your code goes here
    pass
```

**Run the cell below to check your function's output**


```python
# Run this cell unchanged
calculate_skips(df)
```

**Run the cell below to test your function**


```python
# Run this cell unchanged
from tests import test_function
test_function(calculate_skips)
```
