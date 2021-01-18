# using linux here
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
try:
    import httplib
except:
    import http.client as httplib

# This should work on windows and linux
# Make sure to change the chromedriver to have the .exe extension
download_folder_name = "data"
project_path = os.getcwd()
if download_folder_name not in os.listdir(project_path):
    os.mkdir(download_folder_name)
saved_data_path = os.path.join(project_path, download_folder_name)
driver_path = os.path.join(project_path, "chromedriver")
options = webdriver.ChromeOptions()
# options.headless = True
# Set the download Path
prefs = {'download.default_directory': f'{saved_data_path}'}
options.add_experimental_option('prefs', prefs)
yahoo_finance = "https://finance.yahoo.com/quote/"
driver = webdriver.Chrome(driver_path, options=options)


def read_data():
    nasdaq_stocks, s_p = [], []
    with open("nasdaq.txt", "r") as f:
        for line in f.readlines():
            nasdaq_stocks.append(line.strip())
    with open("s.txt", "r") as f:
        for line in f.readlines():
            s_p.append(line.strip())
    all_stocks = nasdaq_stocks + s_p
    return all_stocks


def have_internet():
    conn = httplib.HTTPConnection("www.google.com", timeout=5)
    try:
        conn.request("HEAD", "/")
        conn.close()
        return True
    except:
        conn.close()
        return False


def get_data(symbol='AAPL'):
    try:
        stock_history_link = yahoo_finance + symbol + '/history?p=' + symbol
        driver.get(stock_history_link)
        wait = WebDriverWait(driver, 10)
        wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@class='C($linkColor) Fz(14px)']"))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@data-value='MAX']"))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@class='Fl(end) Mt(3px) Cur(p)']"))).click()
        print(f"{symbol} is downloaded")
        time.sleep(1)
    except:
        print(f"something went wrong when downloading the {symbol} stock")


if __name__ == '__main__':
    try:
        all_stocks = read_data()
        for stock in all_stocks:
            if have_internet():
                get_data(stock)
            else:
                print(f"Trying to get {stock} data")
                print("No Internet Connection, please connect again")
                break
    except:
        print("Something went wrong while running the script")
    finally:
        print("script is done!")
        # driver.quit()
