
from pandas import DataFrame

from app.stockcorrelation import fetch_stocks_csv

def test_fetch_stocks_csv():

    df = fetch_stocks_csv("ABT", "60")

    assert isinstance(df, DataFrame)
    assert df.columns.tolist() == ["timestamp", "open", "high", "low", "close", "adjusted_close", "volume", "dividend_amount", "split_coefficient"]