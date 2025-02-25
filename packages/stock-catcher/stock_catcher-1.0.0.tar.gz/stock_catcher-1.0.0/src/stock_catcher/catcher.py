# Standard library imports
from importlib import resources
from pathlib import Path
from typing import List

# Third party imports
import pandas as pd
import yfinance as yf

# Reader imports
from stock_catcher import CAC40


def get_stock_infos(
    stock_tickers: List[str], add_postfix: bool = False
) -> pd.DataFrame:
    """
    This function takes a list of stock tickers and returns a Pandas DataFrame which contains the basic information of the stock.
    The stock ticker has the following format: <stock_id>.PA. For example: ALO.PA: Alstom, MC.PA: LVMH
    :param add_postfix: If this option is enabled, a postfix ".PA" will be added to the stock ticker. This is for the ticker without .PA such as ALO,
    :param stock_tickers: A list of stock tickers
    :return:
    """
    # We don't need all information of a stock, below is a list of all important columns for me.
    key_columns = [
        "symbol",
        "industry",
        "sector",
        "longBusinessSummary",
        "fullTimeEmployees",
        "auditRisk",
        "boardRisk",
        "compensationRisk",
        "shareHolderRightsRisk",
        "overallRisk",
        "dividendRate",
        "dividendYield",
        "payoutRatio",
        "fiveYearAvgDividendYield",
        "enterpriseValue",
        "fiftyTwoWeekLow",
        "fiftyTwoWeekHigh",
        "fiftyDayAverage",
        "lastDividendValue",
        "lastDividendDate",
        "totalDebt",
        "freeCashflow",
        "operatingCashflow",
        "earningsGrowth",
        "revenueGrowth",
        "grossMargins",
    ]
    stock_infos: List[dict] = []

    # add stock dict into a list
    for stock_ticker in stock_tickers:
        if add_postfix:
            full_name = f"{stock_ticker}.PA"
        else:
            full_name = stock_ticker
        try:
            stock = yf.Ticker(full_name)
            if stock:
                stock_infos.append(stock.info)
        except Exception as e:
            print(f"The stock ticker {stock_ticker} is no longer valid. {e}")
    # convert the list of dict into pandas dataframe, then filter only the column that interests me
    pdf = pd.DataFrame(stock_infos)[key_columns]
    # use symbol column as index
    pdf.set_index("symbol", inplace=True)
    return pdf


def get_top_dividendYield_stock(stock_df, top_n: int = 20) -> pd.DataFrame:
    """
    This function returns the top n dividendYield of a given stock.
    :param stock_df:
    :param top_n:
    :return:
    """
    sortByDiv = stock_df.sort_values(by="dividendYield", ascending=False)
    return sortByDiv.head(top_n)


def get_top_potential_stock(stock_df, top_n: int = 20) -> pd.DataFrame:
    """
    This function returns the top n potential stock of a given stock. We use the (last 52 week high - 50 day average price )/ 52 week high. If the number is positive we keep,
    :param stock_df:
    :param top_n:
    :return:
    """
    stock_df["history_price_diff"] = (
        stock_df["fiftyTwoWeekHigh"] - stock_df["fiftyDayAverage"]
    ) / stock_df["fiftyTwoWeekHigh"]
    stock_df = stock_df.sort_values(by="history_price_diff", ascending=False)
    return stock_df.head(top_n)


def get_fr_stock_tickers(stock_source_path: Path) -> List:
    """
    This function reads a stock symbol file in csv, and returns a list of stock tickers.
    :param stock_source_path: file path of a stock symbol file
    :return:
    """
    if stock_source_path.is_file():
        stock_symbol_pdf = pd.read_csv(stock_source_path.as_posix(), sep=",")
        stock_tickers = stock_symbol_pdf["stock_id"].tolist()
    else:
        raise FileNotFoundError("The provided stock_source_path does not exist")
    return stock_tickers


def get_default_cac_file_path(cac_file_name: str = CAC40) -> Path:
    """
    This function returns the default CAC40 file path. As we use the importlib.resources module, we no longer need to
    consider where this function will be called to get the correct default CAC40 file path. CAC40 is a package default
    variable defined in __init__.py
    :param cac_file_name:
    :return:
    """
    return Path(str(resources.files("stock_catcher.data") / f"{cac_file_name}"))
