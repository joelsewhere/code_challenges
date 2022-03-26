# Parsing json in sql

In this notebook you will
- query an sql database
- write an sql query that parses a json data structure
- write a [common table expression](https://www.geeksforgeeks.org/cte-in-sql/) (CTE) (this is sort of optional, but we talk about them!)
- use a cross join to generate a table of numbers
- write an sql query that parses nested json data

**Below we open a connection to an sqlite database containing data about public holidays in the United States**


```python
# Run this cell unchanged
import sqlite3
from pathlib import Path

db_path = Path('data') / 'holidays.db'
connection = sqlite3.connect(db_path)
```

**Next we define a helper function to make querying the database a bit simpler**


```python
# Run this cell unchanged
import pandas as pd

def run_query(query):
    return pd.read_sql(query, connection)
```

**Now we can run queries by passing a query string into the `run_query` function**


```python
# Run this cell unchanged
q = """

SELECT * 
FROM holidays 
LIMIT 2

"""

run_query(q)
```

## Database Information

### Tables

1. `holidays`
    - Description:
        - This table contains information about public holidays that have been scheduled in the United States. 
    - Columns:
        - year (Integer)
        - data (Varchar)
2. `long_weekends`
    - Description:
        - This table contains information about weekends during which a public holiday has been scheduled in the United States. 
    - Columns:
        - year (Integer)
        - data (Varchar)
        
_Disclaimer: The holidays data is developed programmatically by [this public api](https://date.nager.at/) and is not always 100% accurate, but it does the job for this assignment._

# Task 1 - Write a query that returns the third holiday date for each year

**Let's take a look at the json data in the `holidays` table.**


```python
# Run this cell unchanged
import json

q = """

SELECT data 
FROM holidays 
LIMIT 1

"""

run_query(q).data.apply(json.loads).iloc[0][:4]
```

The sql function we will use to parse this data is [JSON_EXTRACT](https://www.sqlite.org/json1.html#jex).

This function requires a minimum of two arguments.
1. The json data object you would like to parse
2. The "path" for accessing the desired data that is stored in the json data object

The json data above is structured as a **list of dictionaries**. This means there are two datatypes that we need to manipulate.

**Let's take a look at the first datatype. Below is an example of parsing a `list` in sql**

```sql
SELECT 
     --Here we use the JSON_EXTRACT function         
     JSON_EXTRACT('["cat", "dog"]', --The json object is the first argument. It is stored in an sql table as a string
                  
                  '$[0]' /* The second argument is the "path".
                          * This function requires that the path begin with a `$` character. 
                          * The `$` represents a "json object".  
                          * In this case, the `$` represents the list we would like to index.
                          * After the `$` character, we index the list 
                          * exactly how we would index a list in Python */ 
                  
                 ) AS index_0
    
   , JSON_EXTRACT('["cat", "dog"]', '$[1]') AS index_1
```

The comments above are provided to break down the query, but they make the logic of the query a little difficult to read. Below we write out the same query without the comments, and then we run the query!


```python
# Run this cell unchanged
q = """
SELECT 
     JSON_EXTRACT('["cat", "dog"]', '$[0]') AS index_0
   , JSON_EXTRACT('["cat", "dog"]', '$[1]') AS index_1
"""

run_query(q)
```

Take a second to compare the query we just ran with the commented version. How does the query compare with the output?

We just indexed a `list` which is the first part of the query, but the list we are querying is a list of _dictionaries_, and we need to access the `date` variable inside the dictionary. So how to we parse a dictionary?

```postgresql
SELECT 

     JSON_EXTRACT('{"key0":"cat", "key1":"dog"}', /* Like before, the data is stored as a string, 
                                                   * only now it's a dictionary instead of a list */
                  
                  '$.key0' /* The notation for accessing the
                            * value of dictionary is slightly different
                            * in sqlite than it is in python. 
                            * Instead of $['key'] which mirrors python syntax
                            * we use $.key */
                  
                 ) AS value_0
   , JSON_EXTRACT('{"key0":"cat", "key1":"dog"}', '$.key1') AS value_1
   
```

And here is the query without the comments...


```python
# Run this cell unchanged
q = """
SELECT 
     JSON_EXTRACT('{"key0":"cat", "key1":"dog"}', '$.key0') AS value_0
   , JSON_EXTRACT('{"key0":"cat", "key1":"dog"}', '$.key1') AS value_1
"""

run_query(q)
```

Ok, so... 
- we know how to index a list in sql
- we know how to key a dictionary in sql

What if we have a dictionary _inside_ a list. How does that work?

Let's take the dictionary from the above example and make it a nested data structure:
```
[{"key0":"cat"}, {"key0":"dog"}]
```

Here is an example of parsing this nested data...


```python
# Run this cell unchanged
q = """

SELECT 
    JSON_EXTRACT('[{"key0":"cat"}, {"key0":"dog"}]', '$[0].key0') dictionary_0
  , JSON_EXTRACT('[{"key0":"cat"}, {"key0":"dog"}]', '$[1].key0') dictionary_1

"""

run_query(q)
```

## Task 1 - Write your query

In the cell below, write a query that collects the third holiday date for each year

Your query should return an output that looks like this

|    |   year | third_holiday_date   |
|---:|-------:|:---------------------|
|  0 |   2010 | 2010-02-15           |
|  1 |   2011 | 2011-02-21           |
|  2 |   2012 | 2012-02-20           |
|  3 |   2013 | 2013-01-21           |
|  4 |   2014 | 2014-02-17           |
|  5 |   2015 | 2015-02-16           |
|  6 |   2016 | 2016-02-15           |
|  7 |   2017 | 2017-01-20           |
|  8 |   2018 | 2018-02-19           |
|  9 |   2019 | 2019-02-18           |
| 10 |   2020 | 2020-02-17           |
| 11 |   2021 | 2021-01-20           |
| 12 |   2022 | 2022-02-21           |


```python
# Your code goes here
q = """



"""
```


```python
# Run this cell to check your queries output
run_query(q)
```

# Task 2 - Unnest the data

This task is a _total_ level up, but it's where the usage of `JSON_EXTRACT` gets really cool/useful!

The goal for this task is to esssentially expand the `holidays` table vertically, by turning every nested dictionary into an individual row/observation. For those familiar with pandas, we're basically running a `.explode`. 

The important information from the cell below is what the original data looks like, and what it looks like once we've expanded it vertically. 
> I've added comments to the cell below if you'd like to explore how to do this in pandas, but it's not the point of this assignment so you're welcome to run the cell, look at the output, and move on! 


```python
# Run this cell unchanged
from IPython.display import Markdown
display(Markdown('### The original data:'))
display(run_query('select * from holidays'))
display(Markdown('### The vertically expanded data:'))

pd.DataFrame(run_query('select * from holidays') # load the entire holidays tables
 .assign(data=lambda x:x.data.apply(json.loads)) # convert the lists in the data column to actual lists (They are strings in sql)
 .explode('data') # expand the table vertically so each list observation is given its own row
 .data.tolist() # Converting the results to a list of dictionaries so pandas can read the individual dictionaries
).assign(year=lambda x: x.date.str[:4]) # Adding the year column back in
```

**Ok so how do we do this in sql????**

Let's start with talking about **[unions](https://www.w3schools.com/sql/sql_ref_union.asp)** and **[cross joins](https://www.w3resource.com/sql/joins/cross-join.php)**

A **union** takes two tables and merges them vertically. In pandas a union is done via the `pd.concat` function...


```python
# Run this cell unchanged
fake_data_1 = pd.DataFrame([[1,2,3],
                            [4,5,6]])

fake_data_2 = pd.DataFrame([[7,8,9],
                            [10, 11, 12]])

display(Markdown('### Dataset 1'))
display(fake_data_1)
display(Markdown('### Dataset 2'))
display(fake_data_2)
display(Markdown('### Union/Concatenated Data'))
pd.concat([fake_data_1, fake_data_2])
```

In sql, it looks like this...


```python
# Run this cell unchanged
q = """

SELECT 1, 2, 3
UNION ALL
SELECT 4, 5, 6
UNION ALL
SELECT 7, 8, 9
UNION ALL
SELECT 10, 11, 12

"""

run_query(q)
```

Ur probably like, "Cool...but...why are we talking about **unions**???""

Solid question. To unnest the json data, we essentially need to run a **for loop** in sql. This for loop iterates over a range of numbers, and uses each number to index the list of holiday dictionaries in order to pull the data from the list. We will use unions to generate the range of numbers.

In the above example, I coded out every number manually. Does that mean, if we have a list of 100 dictionaries that we need to write out every number from 0-99? Happily, the answer is no. That is what brings us to **cross joins**.

A **cross join** takes two tables and merges every row in table 1 with every row in table 2. In Python, this is oftentimes referred to as finding the "product".


```python
# Run this cell unchanged
from itertools import product

list_1 = [1,2,3]
list_2 = [4,5,6]

list(product(list_1, list_2))
```

The code cell above takes two lists `[1,2,3]` and `[4,5,6]` and then generates every possible combination of two numbers between the data in both lists.

In sql, the two lists represent two seperate tables, and each number represents a row.

Here is the same result in sql...


```python
# Run this cell unchanged
q = """

SELECT * FROM
(          SELECT 1
 UNION ALL SELECT 2
 UNION ALL SELECT 3)
 
CROSS JOIN

(          SELECT 4
 UNION ALL SELECT 5
 UNION ALL SELECT 6)

"""

# Using cursor because column names are not needed
connection.cursor().execute(q).fetchall()
```

Again, you are probably wondering, "how are cross joins relevant to our problem?"

We can use cross joins to expand our list of numbers by cross joining the numbers `0-9` with `10-19` and adding them together.

It looks like this...


```python
# Run this cell unchanged
q = """
SELECT n1.num || ' + ' || (n2.num * 10) || ' =' number1_number2
     , n1.num + n2.num * 10 number_range
FROM
(         SELECT 0 AS num
UNION ALL SELECT 1 AS num
UNION ALL SELECT 2 AS num
UNION ALL SELECT 3 AS num
UNION ALL SELECT 4 AS num
UNION ALL SELECT 5 as num
UNION ALL SELECT 6 as num
UNION ALL SELECT 7 as num
UNION ALL SELECT 8 as num
UNION ALL SELECT 9 as num) n1

CROSS JOIN

(         SELECT 0 AS num
UNION ALL SELECT 1 AS num
UNION ALL SELECT 2 AS num
UNION ALL SELECT 3 AS num
UNION ALL SELECT 4 AS num
UNION ALL SELECT 5 as num
UNION ALL SELECT 6 as num
UNION ALL SELECT 7 as num
UNION ALL SELECT 8 as num
UNION ALL SELECT 9 as num) n2
ORDER BY number_range

"""

run_query(q)
```

The first column above is a string concatenation of the two numbers from each table, and is meant to show you how each number in the `number_range` column is being created. We can increase the numbers in our range by adding a third cross join and multiplying it by 100


```python
# Run this cell unchanged
q = """
SELECT n1.num || ' + ' || (n2.num * 10) || ' + ' || (n3.num * 100) || ' =' number1_number2_number3
     , n1.num + n2.num * 10 + n3.num * 100 number_range
FROM
(SELECT 0 AS num
UNION ALL SELECT 1 AS num
UNION ALL SELECT 2 AS num
UNION ALL SELECT 3 AS num
UNION ALL SELECT 4 AS num
UNION ALL SELECT 5 as num
UNION ALL SELECT 6 as num
UNION ALL SELECT 7 as num
UNION ALL SELECT 8 as num
UNION ALL SELECT 9 as num) n1

CROSS JOIN

(SELECT 0 AS num
UNION ALL SELECT 1 AS num
UNION ALL SELECT 2 AS num
UNION ALL SELECT 3 AS num
UNION ALL SELECT 4 AS num
UNION ALL SELECT 5 as num
UNION ALL SELECT 6 as num
UNION ALL SELECT 7 as num
UNION ALL SELECT 8 as num
UNION ALL SELECT 9 as num) n2

CROSS JOIN

(SELECT 0 AS num
UNION ALL SELECT 1 AS num
UNION ALL SELECT 2 AS num
UNION ALL SELECT 3 AS num
UNION ALL SELECT 4 AS num
UNION ALL SELECT 5 as num
UNION ALL SELECT 6 as num
UNION ALL SELECT 7 as num
UNION ALL SELECT 8 as num
UNION ALL SELECT 9 as num) n3
ORDER BY number_range

"""

run_query(q)
```

Now, you may have noticed that our sql is getting a little...messy. If we continue writing our sql this way, our final solution for this problem is going to become _very_ difficult to read. So let's quickly talk about **[Common Table Expressions](https://www.sqlshack.com/sql-server-common-table-expressions-cte/)** (CTE).

CTE's are mostly designed to improve readability of sql and to help avoid redundancy when writing a query. 

In the above query, we have two steps happening.
1. We create a table of numbers 1-9
2. We query the table of numbers and cross join it with itself

Right now, the 1st step is _inside_ the second step, and it's a little difficult to read. We technically have to read the query from the bottom up in order to read it in the sequential order. Plus, we have to repeat the code for the numbers 1-9 three times, which 1) it's super annoying to write duplicate code and 2) the duplication increases our risk or errors and slows us down if we ever need to update the code in the future.  

**CTE's allow us to** 
- Structure our sql so we can read a query from the top down (we do not have to nest tables inside each other with **subqueries**.)
- Avoid writing the same sql more than once

Let's look at an example:


```python
# Run this cell unchanged
q = """

WITH numbers AS (
                 SELECT 0 AS num
                 UNION ALL SELECT 1 AS num
                 UNION ALL SELECT 2 AS num
                 UNION ALL SELECT 3 AS num
                 UNION ALL SELECT 4 AS num
                 UNION ALL SELECT 5 as num
                 UNION ALL SELECT 6 as num
                 UNION ALL SELECT 7 as num
                 UNION ALL SELECT 8 as num
                 UNION ALL SELECT 9 as num
)
, number_range AS ( SELECT n1.num || ' + ' || (n2.num * 10) || ' + ' || (n3.num * 100) || ' =' number1_number2_number3
                         , n1.num + n2.num * 10 + n3.num * 100 AS number_range
                    FROM numbers n1
                    CROSS JOIN numbers n2
                    CROSS JOIN numbers n3
                    ORDER BY number_range
)
SELECT * FROM number_range

"""

run_query(q)
```

In the above query...
1. We tell the computer we would like to use CTE's via the `WITH` command
1. We define a table called `numbers` that contains the numbers `1-9`
1. We define a table called `number_range` that cross joins the `numbers` table with itself three times

The general syntax for a CTE is 

```mysql

WITH <table_name> AS (<query>), <table_name> AS (<query>), <table_name> AS (<query>) <FINAL OUTPUT QUERY>
```

Ok so with this in mind, let's use CTEs to write out the rest of our query...

Before we write out the final query, let's take a look at how we turn this range of numbers into a "for loop"


```python
# Run this cell unchanged
run_query('select * from long_weekends limit 1')
```

Let's say we want to expand json data in the output below so each dictionary has its own row. For now we will just grab the `startDate` and `endDate` for each dictionary.

We can do this by...
1. Defining a range of numbers that encompass the length of the list of dictionaries
2. Cross joining the list of dictionaries with the range of numbers
3. Passing the number from the range of numbers into `JSON_EXTRACT`.


```python
# Run this cell unchanged
q = """

WITH numbers AS (
                 SELECT 0 AS num
                 UNION ALL SELECT 1 AS num
                 UNION ALL SELECT 2 AS num
                 UNION ALL SELECT 3 AS num
                 UNION ALL SELECT 4 AS num
                 UNION ALL SELECT 5 as num
                 UNION ALL SELECT 6 as num
                 UNION ALL SELECT 7 as num
                 UNION ALL SELECT 8 as num
                 UNION ALL SELECT 9 as num
)
, for_loop AS (
                SELECT 0 + n1.num + n2.num * 10 + n3.num * 100 AS i
                FROM numbers n1
                CROSS JOIN numbers n2
                CROSS JOIN numbers n3
                ORDER BY i
                )
SELECT
       JSON_EXTRACT(l.data, '$['|| loop.i || '].startDate') start_date
     , JSON_EXTRACT(l.data, '$['|| loop.i || '].endDate') end_date
     , l.year
FROM (SELECT * FROM long_weekends LIMIT 1) l 
CROSS JOIN for_loop loop
"""

run_query(q)
```

Looking at the output above, we have a bunch of values with no `start_date` or `end_date`. This is because we are looping over the numbers `1-1000` and 2010 did not have 1,000 long weekends. We can avoid this by either filtering out nulls in the final query or by limiting the size of the `for_loop` table.

### Task 2 - Write your query

Ok, time for you to do some pattern matching and write out a query that vertically expands the holidays table! The code should be very similar to the query above!

As a reminder, your query should return data that looks like the following output via pandas:


```python
# Run this cell unchanged
pd.DataFrame(run_query('select * from holidays')
 .assign(data=lambda x:x.data.apply(json.loads))
 .explode('data')
 .data.tolist() 
).assign(year=lambda x: x.date.str[:4])
```


```python
# Your code here
q = """



"""
```


```python
# Run this cell to check your query's output
run_query(q)
```
