def get_price():
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
    company = sys.argv[1].lower()
    stock_name = None
    for company_name, stocks in COMPANIES.items():
        if company_name.lower() == company:
            stock_name = stocks
            break
    if stock_name:
        print(STOCKS[stock_name])
    else:
        print("Unknown company")

if __name__ == '__main__':
    get_price()

