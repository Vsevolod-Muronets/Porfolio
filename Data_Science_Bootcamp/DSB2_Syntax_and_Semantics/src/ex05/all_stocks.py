def search_by_val_or_key():
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

    input_str = sys.argv[1]
    for_check = input_str.replace(" ", "")
    if ',,' in for_check:
        return

    expressions = [expr.strip() for expr in input_str.split(',')]
    for expr in expressions:
        expr_lcase = expr.lower()
        found = False
        for comp_name, ticker in COMPANIES.items():
            if expr_lcase == ticker.lower():
                print(f"{ticker} is a ticker symbol for {comp_name}")
                found = True
                break
        if not found:
            for comp_name, ticker in COMPANIES.items():
                if expr_lcase == comp_name.lower():
                    print(f"{comp_name} stock price is {STOCKS[ticker]}")
                    found = True
                    break
        if not found:
            print(f"{expr} is an unknown company or an unknown ticker symbol")

if __name__ == '__main__':
    search_by_val_or_key()

