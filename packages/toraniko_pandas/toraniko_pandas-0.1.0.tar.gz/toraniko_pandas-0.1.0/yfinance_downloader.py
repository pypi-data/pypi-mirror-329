# %%
import os
import pickle
import zipfile

import pandas as pd
import yfinance as yf
from tqdm import tqdm

from toraniko_pandas.utils import fill_features

pd.set_option("future.no_silent_downcasting", True)
# disable scientific notation
pd.set_option("display.float_format", lambda x: "%.5f" % x)


def fill_series(series: pd.Series) -> pd.Series:
    """Fill missing values in a series using the specified method."""
    series = pd.to_numeric(series, errors="coerce")
    series = series.replace([np.inf, -np.inf], np.nan)
    series = series.ffill()

    return series


def download_sp500_tickers(save_path="cached_data/sp500_tickers.csv"):
    """
    Download the S&P 500 tickers from Wikipedia and save them locally as a CSV file.

    Args:
        save_path (str): The path where the CSV file will be saved.
    """
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    sp500 = pd.read_html(url)[0]
    sp500_tickers = sp500["Symbol"].to_list()
    sp500_tickers = [ticker.replace(".", "-") for ticker in sp500_tickers]

    # Save the tickers to a CSV file
    pd.DataFrame(sp500_tickers, columns=["Ticker"]).to_csv(save_path, index=False)
    print(f"S&P 500 tickers saved to {save_path}")


def load_sp500_tickers(file_path="sp500_tickers.csv"):
    """
    Loads the S&P 500 tickers from a CSV file.

    Args:
        file_path (str): The path to the CSV file containing the tickers.

    Returns:
        list: A list of S&P 500 tickers.
    """
    sp500_tickers = pd.read_csv(file_path)["Ticker"].to_list()
    sp500_tickers = [ticker.replace(".", "-") for ticker in sp500_tickers]
    return sp500_tickers


class Stock:
    def __init__(self, ticker):
        """
        Initialize the Stock class with a ticker symbol.
        """
        self.ticker = ticker
        self.outer_zip_path = "cached_data/tickers.zip"
        self.inner_zip_path = f"{ticker}.zip"
        self.features = []
        self.dfs = []
        self.load_data()

    def load_data(self):
        """
        Load stock data from a zip file if it exists, otherwise download the data.
        """
        if os.path.exists(self.outer_zip_path):
            with zipfile.ZipFile(self.outer_zip_path, "r") as outer_zip:
                if self.inner_zip_path in outer_zip.namelist():
                    with outer_zip.open(self.inner_zip_path, "r") as inner_zip_file:
                        with zipfile.ZipFile(inner_zip_file) as inner_zip:
                            with inner_zip.open(f"{self.ticker}_data.pkl", "r") as file:
                                data = pickle.load(file)
                                for key, value in data.items():
                                    setattr(self, key, value)
                else:
                    self.download_data()
        else:
            self.download_data()

    def download_data(self):
        """
        Download stock data from Yahoo Finance and save it locally.
        """
        self.stock = yf.Ticker(self.ticker)
        self.sector = self.stock.info.get("sector", "N/A")
        self.industry = self.stock.info.get("industry", "N/A")
        self.end_date = pd.Timestamp.now()
        self.start_date = "2012-12-31"

        self.all_financials = pd.concat(
            [
                self.stock.income_stmt,
                self.stock.balance_sheet,
                self.stock.cash_flow,
            ],
            axis=0,
        )
        self.all_financials_quarterly = pd.concat(
            [
                self.stock.quarterly_income_stmt,
                self.stock.quarterly_balance_sheet,
                self.stock.quarterly_cash_flow,
            ],
            axis=0,
        )
        self.get_prices()
        self.save_data()

    def save_data(self):
        """
        Save stock data to a zip file.
        """
        data = {
            "sector": self.sector,
            "industry": self.industry,
            "end_date": self.end_date,
            "start_date": self.start_date,
            "all_financials": self.all_financials,
            "all_financials_quarterly": self.all_financials_quarterly,
            "prices": self.prices,
            "tz": self.tz,
        }
        with zipfile.ZipFile(self.outer_zip_path, "a") as outer_zip:
            with outer_zip.open(self.inner_zip_path, "w") as inner_zip_file:
                with zipfile.ZipFile(inner_zip_file, "w") as inner_zip:
                    with inner_zip.open(f"{self.ticker}_data.pkl", "w") as file:
                        pickle.dump(data, file)

    def get_returns(self, price_type="open"):
        """
        Calculate and store the returns for the stock.
        """
        self.returns_df = (
            self.prices[price_type]
            .pct_change()
            .to_frame(name="asset_returns")
            .assign(symbol=self.ticker, sector=self.sector, industry=self.industry)
        )
        self.features.append("asset_returns")
        self.dfs.append(self.returns_df)

    def prepare_data(
        self,
        freq="annual",
        lag_periods=1,
        price_type="open",
        share_type="Ordinary Shares Number",
        book_variable="Common Stock Equity",
        sales_variable="Total Revenue",
        cf_variable="Free Cash Flow",
    ):
        """
        Prepare the data for the stock by calculating returns, market cap, and value metrics.
        """
        self.get_returns()

        self.get_market_cap(
            freq=freq,
            share_type=share_type,
            lag_periods=lag_periods,
            price_type=price_type,
        )
        self.get_value_metrics(
            freq=freq,
            book_variable=book_variable,
            sales_variable=sales_variable,
            cf_variable=cf_variable,
            lag_periods=lag_periods,
        )

        full_df = pd.concat(self.dfs, axis=1)

        full_df_filled = fill_features(
            full_df,
            self.features,
            sort_col="date",
            over_col="symbol",
        )

        return full_df_filled

    def get_value_metrics(
        self, book_variable, sales_variable, cf_variable, freq, lag_periods
    ):
        """
        Calculate and store the value metrics for the stock.
        """
        book_value = self._get_variable(
            variable=book_variable,
            freq=freq,
            lag_periods=lag_periods,
            name="book_value",
        )
        sales = self._get_variable(
            variable=sales_variable,
            freq=freq,
            lag_periods=lag_periods,
            name="sales",
        )
        cash_flow = self._get_variable(
            variable=cf_variable,
            freq=freq,
            lag_periods=lag_periods,
            name="cash_flow",
        )

        value_df = pd.concat([book_value, sales, cash_flow], axis=1)

        value_df = value_df.div(self.market_cap_df["market_cap"], axis=0)
        value_df.columns = ["book_price", "sales_price", "cf_price"]

        self.dfs.append(value_df)
        self.features += ["book_price", "sales_price", "cf_price"]
        self.value_df = value_df

    def get_market_cap(
        self,
        share_type,
        freq,
        lag_periods,
        price_type,
    ):
        """
        Calculate and store the market cap for the stock.
        """
        shares_outstanding = self._get_variable(
            variable=share_type,
            freq=freq,
            lag_periods=lag_periods,
        )
        prices = self.prices[price_type]
        market_cap = shares_outstanding.mul(prices, axis=0).set_axis(
            ["market_cap"], axis=1
        )

        self.features.append("market_cap")
        self.dfs.append(market_cap)
        self.market_cap_df = market_cap

    def get_prices(self):
        """
        Download and store the historical prices for the stock.
        """
        self.prices = self.stock.history(
            period="1d",
            interval="1d",
            start=self.start_date,
            end=self.end_date,
            repair=True,
            auto_adjust=True,
        )

        self.prices.columns = [
            col.lower().replace(" ", "_").replace(".", "").replace("?", "")
            for col in self.prices.columns
        ]
        self.prices.index.name = self.prices.index.name.lower().replace(" ", "_")
        self.tz = self.prices.index.tz

    def _get_variable(
        self,
        variable,
        freq="annual",
        lag_periods=1,
        name=None,
    ):
        """
        Get a financial variable for the stock, resample it, and align it with the price data.
        """
        if freq == "quarterly":
            data = self.all_financials_quarterly.loc[variable]
            data = data.sort_index()
            data.index += pd.DateOffset(months=lag_periods * 3)
            data = data.dropna()
        elif freq == "annual":
            data = self.all_financials.loc[variable]
            data = data.sort_index()
            data.index += pd.DateOffset(years=lag_periods)
            data = data.dropna()
        else:
            raise ValueError("freq must be 'quarterly' or 'annual'")

        data.index = data.index.tz_localize(self.tz)
        data = data.resample("B").bfill().reindex(self.prices.index)
        data = fill_series(data)

        if name:
            return data.to_frame(name=name)
        return data.to_frame()

    def _date_offset(self, freq, lag_periods):
        """
        Offset the date index by a number of periods based on the frequency.
        """
        if freq == "quarterly":
            return pd.DateOffset(months=lag_periods * 3)
        elif freq == "annual":
            return pd.DateOffset(years=lag_periods)
        else:
            raise ValueError("freq must be 'quarterly' or 'annual'")

    def _resample(self, data):
        """
        Resample the data based on the frequency.
        """
        return data.resample("B").bfill().reindex(self.prices.index)


class Stocks:
    def __init__(self, new_tickers=[]):
        """
        Initialize the Stocks class with a list of new tickers.
        """
        self.outer_zip_path = "cached_data/tickers.zip"
        self.saved_tickers = self.get_cached_tickers()
        self.load_tickers(new_tickers)

    def __repr__(self) -> str:
        """
        Return a string representation of the Stocks class.
        """
        return f"Cached tickers: {len(self.saved_tickers)})"

    def load_tickers(self, tickers):
        """
        Load data for a list of tickers.
        """
        tickers = set(tickers) - set(self.saved_tickers)
        for ticker in tqdm(tickers, desc=f"Loading {len(tickers)} tickers"):
            _ = Stock(ticker)

    def build_factor_data(self):
        """
        Build factor data for the cached tickers.
        """
        data_frames = []
        for ticker in tqdm(self.saved_tickers, desc="Building factor data"):
            stock = Stock(ticker)
            data_frames.append(stock.prepare_data())
        factor_data = pd.concat(data_frames)
        factor_data.to_pickle("cached_data/factor_data.pkl")

    def load_factor_data(self):
        """
        Load factor data from a pickle file if it exists, otherwise build the factor data.
        """
        if os.path.exists("cached_data/factor_data.pkl"):
            factor_data = pd.read_pickle("cached_data/factor_data.pkl")
            factor_tickers = factor_data["symbol"].unique().tolist()
            if not set(factor_tickers) >= set(self.saved_tickers):
                print("Factor data is outdated. Building factor data...")
                self.build_factor_data()
                factor_data = pd.read_pickle("cached_data/factor_data.pkl")
            print("Factor data loaded")
            return factor_data
        else:
            print("Factor data not found. Building factor data...")
            self.build_factor_data()
            factor_data = pd.read_pickle("cached_data/factor_data.pkl")
            return factor_data

    def get_cached_tickers(self):
        """
        Get the list of cached tickers from the zip file.
        """
        with zipfile.ZipFile(self.outer_zip_path, "r") as outer_zip:
            return [
                file.replace(".zip", "")
                for file in outer_zip.namelist()
                if ".zip" in file
            ]


if __name__ == "__main__":
    sp500_tickers = load_sp500_tickers("cached_data/sp500_tickers.csv")
    stocks = Stocks()
    stocks.build_factor_data()
    # remaining_tickers = list(set(sp500_tickers) - set(stocks.saved_tickers))
    # tickers = np.random.choice(remaining_tickers, 2)
    # stocks.load_tickers(remaining_tickers)
    # factor_data = stocks.load_factor_data()
    # print(len(factor_data.symbol.unique()))

# %%
