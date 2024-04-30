import requests
from datetime import datetime
import time
import os
import csv
from io import StringIO
import sqlite3


def scraper(ticker: object, from_date: object, to_date: object) -> object:
    # Convert the dates to datetime objects
    from_datetime = datetime.strptime(from_date, '%Y/%m/%d')
    to_datetime = datetime.strptime(to_date, '%Y/%m/%d')

    # Convert the datetime objects to timestamps
    from_epoch = int(time.mktime(from_datetime.timetuple()))
    to_epoch = int(time.mktime(to_datetime.timetuple()))

    url = f"https://query1.finance.yahoo.com/v7/finance/download/{ticker}?period1={from_epoch}&period2={to_epoch}&interval=1d&events=history&includeAdjustedClose=true"

    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36"}

    content = requests.get(url, headers=headers).content
    content = content.decode('utf-8')



    # Read the content of the response
    data = []
    reader = csv.DictReader(StringIO(content))
    for row in reader:
        # Create a dictionary for each row
        row_dict = {
            'date': row['Date'],
            'open': row['Open'],
            'high': row['High'],
            'low': row['Low'],
            'close': row['Close'],
            'adj_close': row['Adj Close'],
            'volume': row['Volume'],
        }
        data.append(row_dict)
        with open('stock_data.csv', 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=row_dict.keys())
            writer.writeheader()
            writer.writerows(data)

    return data

def read_csv_file(file_path):
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        data = [row for row in reader]
    return data

def save_data_to_db(data, db_path):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS stock_data (
            date text,
            open real,
            high real,
            low real,
            close real,
            adj_close real,
            volume integer
        )
    ''')

    for row in data:
        c.execute('''
            INSERT INTO stock_data VALUES (
                :date,
                :open,
                :high,
                :low,
                :close,
                :adj_close,
                :volume
            )
        ''', row)

    conn.commit()
    conn.close()



if __name__ == "__main__":
    main()
