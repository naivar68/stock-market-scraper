import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
from stock_scraper import scraper
from csv import DictWriter
import csv
import sqlite3
from stock_scraper import read_csv_file, save_data_to_db



def get_tickers_and_company_names():
    tickurl = 'https://finance.yahoo.com/most-active'
    headers = { "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36"}
    response = requests.get(tickurl, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    tickers = {}
    ticker_elements = soup.find_all('a', class_='Fw(600)')
    company_name_elements = soup.find_all('td', class_='Va(m) Ta(start) Px(10px) Fz(s)')

    for ticker_element, company_name_element in zip(ticker_elements, company_name_elements):
        ticker = ticker_element.text
        company_name = company_name_element.text
        tickers[ticker] = company_name

    return tickers



def save_data_to_csv(data):
    with open('stock_data.csv', 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)



def main():
    os.system('clear' if os.name == 'posix' else 'cls')
    query = input("Do you want to scrape stock data? (y/n): ")
    if query.lower() == 'y':
        tickers = get_tickers_and_company_names()
        print("Here are the tickers and their company names:")
        for ticker, company_name in tickers.items():
            print(f"{ticker}: {company_name}")
        ticker = input("Enter the ticker you want to scrape data for: ")
        from_date = input("Enter the from date (yyyy/mm/dd): ")
        to_date = input("Enter the to date (yyyy/mm/dd): ")
        data = scraper(ticker, from_date, to_date)
        data = read_csv_file('stock_data.csv')
        save_data_to_db(data, 'stock_data.db')

    else:
        print("Exiting program...")



if __name__ == '__main__':
    main()