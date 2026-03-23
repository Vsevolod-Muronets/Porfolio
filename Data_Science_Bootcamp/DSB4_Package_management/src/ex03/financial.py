#!/usr/bin/env python3

import sys
from bs4 import BeautifulSoup
import requests
import time
import socket

def finances():

    time.sleep(5)

    if len(sys.argv) != 3:
        raise ValueError("Wrong number of arguments. Correct usage: ./financial.py <Ticker_name> <Field_name>")

    ticker = sys.argv[1].upper()
    field = sys.argv[2]
    ticker_lower = ticker.lower()

    url = f"https://finance.yahoo.com/quote/{ticker}/financials/?p={ticker_lower}"
    
    headers = {
        'User-Agent': ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "  "AppleWebKit/537.36 (KHTML, like Gecko) " "Chrome/128.0.0.0 Safari/537.36"),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    }

    try:
        socket.create_connection(("8.8.8.8", 53), timeout=3)
    except OSError as e:
        raise ConnectionError("No internet connection") from e

    response = requests.get(url, headers = headers)
    if response.status_code != 200:
        raise ConnectionError(f'Unable to connect correctly. Connection status: {response.status_code}')
    soup_obj = BeautifulSoup(response.text, 'html.parser')
    table = soup_obj.find('div', class_ = 'tableBody yf-yuwun0')
    if table == None:
        raise TypeError(f"Wrong ticker is used: {sys.argv[1]}\nOr you were redirected. Check the URL: {response.url}")
    needed_rows = table.find_all('div', class_ = 'row lv-0 yf-t22klz')

    final_tuple = ()
    for row in needed_rows:
        field_name = row.find('div', class_ = 'column sticky yf-t22klz').text.strip()
        if field_name == field:
            vals = row.find_all('div', class_ = ['column yf-t22klz', 'column yf-t22klz alt'])
            final_tuple = tuple([field_name] + [val.text.strip() for val in vals])
            print(final_tuple)

    if final_tuple == ():
        raise KeyError(f"Requested field {field} does not exist")

if __name__ == "__main__":
    try:
        finances()
    except (ValueError, ConnectionError, KeyError, TypeError) as exc:
        print(f"{str(exc)}")
        sys.exit(1)
