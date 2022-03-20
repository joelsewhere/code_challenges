import pandas as pd
import sqlite3
import re
import os

pardir = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir))
db_path = os.path.join(pardir, 'data', 'tests.db')
connection = sqlite3.connect(db_path)

def test_query(query):
    tables = [x[0] for x in (connection.cursor()
                                       .execute("SELECT name FROM sqlite_master WHERE type='table' AND not substr(name, -2) = '__';")
                                       .fetchall())]
    correct = 0
    for table in tables:
        # Using regex to replace the table being queried
        test_query = re.sub('from\s+tasks', f'from {table}', query.lower().replace('\n', ' '))
        test_answer = pd.read_sql(test_query, connection)
        test_solution = pd.read_sql(f'select * from {table}__ order by person', connection)
        if test_answer.equals(test_solution):
            correct += 1
    print(f'{correct}/{len(tables)} tests were passed.')
        
    
    
    
    