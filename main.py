import requests
from bs4 import BeautifulSoup
import pandas as pd
import io
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.cryptocurrencies import CryptoCurrencies

class AlphaVantageAPI:
    def __init__(self, api_key_file):
        with open(api_key_file) as file:
            self.API_KEY = file.read().strip()
        self.ts = TimeSeries(key=self.API_KEY)
        self.cc = CryptoCurrencies(key=self.API_KEY)

    def get_monthly_stock_data(self, symbol):
        return self.ts.get_monthly(symbol)

    def get_weekly_stock_data(self, symbol):
        return self.ts.get_weekly(symbol)

    def get_intraday_stock_data(self, symbol):
        return self.ts.get_intraday(symbol)

    def get_weekly_stock_data_df(self, symbol):
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol={symbol}&apikey={self.API_KEY}&datatype=csv'
        r = requests.get(url).content
        data = pd.read_csv(io.StringIO(r.decode("utf-8")))
        return data

    def get_income_statement(self, symbol):
        url = f'https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol={symbol}&apikey={self.API_KEY}'
        r = requests.get(url)
        return BeautifulSoup(r.content, features="html.parser")

    # Add other functions for different API endpoints as needed

def main():
    api_key_file = "API_key.txt"
    alpha_vantage = AlphaVantageAPI(api_key_file)

    symbol = input("Please enter a stock symbol: ")

    #symbol = "AAPL"

    monthly_data = alpha_vantage.get_monthly_stock_data(symbol)
    weekly_data = alpha_vantage.get_weekly_stock_data(symbol)
    intraday_data = alpha_vantage.get_intraday_stock_data(symbol)
    weekly_data_df = alpha_vantage.get_weekly_stock_data_df(symbol)
    income_statement = alpha_vantage.get_income_statement(symbol)

    # Use the data as needed
    print(f"\nHere is the weekly stock data for {symbol}\n")    
    print(weekly_data_df)

    print(f"\nHere is the monthly stock data for {symbol}\n")    
    print(monthly_data)

    print(f"\nHere is the income statement for {symbol}\n")    
    print(income_statement)

if __name__ == "__main__":
    main()