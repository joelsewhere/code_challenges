import string
import json
import string
import os
import sqlite3
import numpy as np
import pandas as pd
from tqdm import trange

def load_options():
    pardir = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir))
    options_path = os.path.join(pardir, 'data', 'task_names.json')
    file = open(options_path, 'r')
    options = json.load(file)
    file.close()
    
    return options


def generate_task_names(options):

    tasks = ['-'.join(options[np.random.choice(range(len(options)))]) for x in range(np.random.choice(range(20, 100)))]
    tasks_and_ordinality = list(zip(tasks, range(len(tasks))))
    
    return tasks_and_ordinality

def generate_people(tasks):

    people = []

    for letter in string.ascii_uppercase[:np.random.choice(range(2, int(len(tasks) * .25)))]:
        people.append('Person {}'.format(letter))
    
    return people

def generate_data(tasks, people):
    
    data = []

    for task in tasks:
        for person in people:
            data.append([person, *task])

    frame = (pd.DataFrame(data, columns=['person', 'task_name', 'ordinality'])
             .sort_values(['person', 'ordinality'])
             .assign(completed = np.random.choice([False,True], 
                                                   p=[.10, .90], 
                                                   size=len(data))))
    return frame

def _(dataframe):
    return (dataframe.sort_values('ordinality', ascending=False)
           .assign(cumulative=lambda x: x.groupby('person').completed.cumsum(),
                   skipped=lambda x: x.apply(lambda y: True if not y.completed 
                                                            and y.cumulative > 0 
                                                            else False, axis=1))
           .groupby('person').skipped.sum()).to_frame().reset_index()

def create_tests_db(data, name):
    pardir = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir))
    path = os.path.join(pardir, 'data', 'tests.db')
    connection = sqlite3.connect(path)
    data.to_sql(name, connection, index=False, if_exists='replace')
    __ = _(data)
    __.to_sql(name + '__', connection, index=False, if_exists='replace')

def generate_test_data(num_test_datasets=20):
    options = load_options()
    
    for num in trange(num_test_datasets):
        tasks = generate_task_names(options)
        people = generate_people(tasks)
        data = generate_data(tasks, people)
        create_tests_db(data, 'dataset_' + str(num))