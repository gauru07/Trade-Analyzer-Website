import pandas as pd
import numpy as np
from datetime import datetime, timedelta




def random_datetime(start, end):
    delta = end - start
    random_days = np.random.uniform(0, delta.days)
    random_seconds = np.random.uniform(0, delta.seconds)
    return start + timedelta(days=random_days, seconds=random_seconds)




def generate():
    np.random.seed(42)
    rows = []
    stocks_holding = {} 

    start_datetime = datetime(2023, 6, 1)
    end_datetime = datetime(2023, 6, 30)

    for i in range(1000):
        Datetime = random_datetime(start_datetime, end_datetime)

        stock = np.random.choice(['INFY', 'RELIANCE', 'TCS'])

        ordertype = np.random.choice(['Buy', 'Sell'])

        if ordertype == 'Buy':
            if stock in stocks_holding:

                continue
            else:

                quantity = round(np.random.uniform(10, 100))
                stocks_holding[stock] = quantity 
        else:
            if stock in stocks_holding:

                quantity = stocks_holding[stock]
                stocks_holding.pop(stock)  
            else:

                continue

        if stock == 'INFY':
            price = round(np.random.uniform(1200, 1500), 2)

        if stock == 'RELIANCE':
            price = round(np.random.uniform(2000, 3000), 2)

        if stock == 'TCS':
            price = round(np.random.uniform(3000, 4000), 2)

        exchange = 'NSE'
        rows.append([Datetime, stock, ordertype, price, quantity, exchange])

    df = pd.DataFrame(rows, columns=['datetime', 'stock', 'ordertype', 'price', 'quantity', 'Exchange'])
    df = df.sort_values(by='datetime').reset_index(drop=True)  # Sort by datetime in increasing order
    df.to_csv('sample_data.csv', index=False)

if(__name__=="__main__"):
    generate()
