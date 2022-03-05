import pandas as pd
import numpy as np
import sqlite3

conn = sqlite3.connect('orders.db')

orders = pd.read_sql('select * from orders', conn)
customers = pd.read_sql('select * from customer_activity', conn)

def test(query):
    
    query_results = pd.read_sql(query, conn)
    
    query_results = query_results.assign(cumulative_total=np.round(query_results.cumulative_total, 2))
    
    answer = (customers.merge(orders, on='order_id')
     .sort_values('date')
     .assign(cumulative_total=lambda x: np.round(x.groupby('customer_id').cumsum(), 2))
     .drop(['amount_spent', 'order_id'],axis=1))
    
    if (answer.to_numpy() == query_results.to_numpy()).all():
        print('✅ Correct!')
    else:
        if query_results.shape != answer.shape:
            print('❌ incorrect')
            print(f'Your query produced a table with the shape {query_results.shape}'
                  f'but should have produced a table with the shape {answer.shape}')
        elif not query_results.sort_values('date').equals(query_results):
            print('❌ incorrect')
            print('Be sure to sort your data!')
        else:
            print('❌ incorrect')


