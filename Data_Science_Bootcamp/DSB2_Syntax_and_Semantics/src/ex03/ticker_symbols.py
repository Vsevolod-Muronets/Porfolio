def get_name_and_price():
    import sys

    if len(sys.argv) != 2:
        return

    COMPANIES = {
    'Apple': 'AAPL',
    'Microsoft': 'MSFT',
    'Netflix': 'NFLX',
    'Tesla': 'TSLA',
    'Nokia': 'NOK'
    }

    STOCKS = {
    'AAPL': 287.73,
    'MSFT': 173.79,
    'NFLX': 416.90,
    'TSLA': 724.88,
    'NOK': 3.37
    }

    stock_name = sys.argv[1].upper()
    company = None
    for company_name, stock in COMPANIES.items():
        if stock == stock_name:
            company = company_name
            break
    if company:
        print(f"{company} {STOCKS[stock_name]}")
    else:
        print("Unknown ticker")

if __name__ == '__main__':
    get_name_and_price()


