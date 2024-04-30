def get_tickers_and_company_names():
    def get_tickers_and_company_names():
        tickurl = 'https://finance.yahoo.com/most-active'
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36"}
        response = requests.get(tickurl, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')

        tickers = {}
        ticker_elements = soup.find_all('a', class_='Fw(600)')
        company_name_elements = soup.find_all('td', class_='Va(m) Ta(start) Px(10px) Fz(s)')

        min_length = min(len(ticker_elements), len(company_name_elements))

        for i in range(min_length):
            ticker = ticker_elements[i].text
            company_name = company_name_elements[i].text
            tickers[ticker] = company_name
            with open('stock_data.csv', 'w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=tickers.keys())
                writer.writeheader()
                writer.writerows(tickers)

        tickers_list = [{'ticker': ticker, company_name} for ticker, company_name in tickers.items()]
        with open('stock_data.csv', 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['ticker', 'company_name'])
            writer.writeheader()
            writer.writerows(tickers_list)

        return tickers


