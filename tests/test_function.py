import pandas as pd
import sqlite3
import os

pardir = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir))
db_path = os.path.join(pardir, 'data', 'tests.db')
connection = sqlite3.connect(db_path)

def test_function(function):
    tables = [x[0] for x in (connection.cursor()
                                       .execute("SELECT name FROM sqlite_master WHERE type='table' AND not substr(name, -2) = '__';")
                                       .fetchall())]
    correct = 0
    for table in tables:
        test_table = pd.read_sql(f'select * from {table}', connection)
        test_answer = function(test_table)
        test_solution = pd.read_sql(f'select * from {table}__ order by person', connection)
        if test_answer.equals(test_solution):
            correct += 1
    print(f'{correct}/{len(tables)} tests were passed.')