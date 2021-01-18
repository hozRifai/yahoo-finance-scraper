# scraping yahoo finance data
import os
import requests
import datetime
from time import sleep
from bs4 import BeautifulSoup

yahoo_finance = "https://finance.yahoo.com/quote/"

def get_data(symbol='AAPL'):
    stock_history_link = yahoo_finance + symbol
    end = int(datetime.datetime.strptime(datetime.date.today().isoformat(), "%Y-%m-%d").timestamp())
    url = f"{stock_history_link}/history?period1=000000000&period2={end}" \
          f"&interval=1d&filter=history&frequency=1d&includeAdjustedClose=true"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    table = soup.find("table", class_="W(100%) M(0)")
    print("table", table)
    rows = table.find_all("tr")
    print("rows are: ", rows)
    for row in rows:
        td = row.find_all("td")
        if len(td) > 5:
            for x in td:
                print(x.text)

if __name__ == '__main__':
    try:
        get_data()
    except:
        pass
    finally:
        print("script is finished")