import sys
from stock_catcher.catcher import *

print("Executing __main__.py")

def main():
    """Read the stock file and run the stock catcher."""

    # If user provides a file, then use the given file path
    if len(sys.argv) > 1:
        stock_file_path = Path(sys.argv[1])
    # if nothing provided, use the default file path
    else:
        stock_file_path = get_default_cac_file_path()
    try:
        stock_tickers = get_fr_stock_tickers(stock_file_path)
        stock_info_pdf = get_stock_infos(stock_tickers)
    except FileNotFoundError:
        print(f"The given file path {stock_file_path.as_posix()} not found")
        sys.exit(1)
    print(stock_info_pdf)
    top_div=get_top_dividendYield_stock(stock_info_pdf)
    top_pot = get_top_potential_stock(stock_info_pdf)
    print(f"Top Dividend:\n{top_div}")
    print(f"Top potential:\n{top_pot}")

if __name__ == "__main__":
    main()