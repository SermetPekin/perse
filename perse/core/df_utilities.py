"""
MIT License
Package: perse
Copyright (c) 2024 Sermet Pekin

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from .base import BaseDataFrame
import pandas as pd
import polars as pl


class DataFrameLocator:
    """DataFrameLocator"""

    def __init__(self, parent_df):
        self.parent_df = parent_df

    def __getitem__(self, key):
        self.parent_df.refresh_pandas()
        result = self.parent_df._df.loc[key]
        if isinstance(result, pd.DataFrame):
            return self.parent_df.final_copy(dl=pl.DataFrame(result))
        elif isinstance(result, pd.Series):
            return self.parent_df.final_copy(dl=pl.DataFrame(result.to_frame()))
        else:
            return result


class IDataFrameLocator:
    """DataFrameLocator"""

    def __init__(self, parent_df):
        self.parent_df = parent_df

    def __getitem__(self, key):
        self.parent_df.refresh_pandas()
        result = self.parent_df._df.iloc[key]
        if isinstance(result, pd.DataFrame):
            return self.parent_df.final_copy(dl=pl.DataFrame(result))
        elif isinstance(result, pd.Series):
            return self.parent_df.final_copy(dl=pl.DataFrame(result.to_frame()))
        else:
            return result


class UtilitiesDataFrame(BaseDataFrame):
    """UtilitiesDataFrame"""

    def refresh_pandas(self):
        """refresh_pandas"""
        if not self._is_df_fresh:
            self._df = self.dl.to_pandas()
            self._is_df_fresh = True

    @property
    def df(self) -> pd.DataFrame:
        """ df """
        self.refresh_pandas()
        return self._df

    def add_column(self, name: str, values, inplace=False):
        """add_column """

        if inplace:
            if self.locked:
                return self.locked_message()

            self.dl = self.dl.with_columns(pl.Series(name, values))
            self._is_df_fresh = False
            return self
        else:
            obj = self.copy()
            obj.dl = obj.dl.with_columns(pl.Series(name, values))
            obj._is_df_fresh = False
            return obj

    def filter_rows(self, condition, inplace=False):
        """filter_rows"""
        if inplace:
            if self.locked:
                return self.locked_message()

            self.dl = self.dl.filter(condition)
            self._is_df_fresh = False
            return self
        else:
            obj = self.copy()
            obj.dl = obj.dl.filter(condition)
            obj._is_df_fresh = False
            return obj

    def to_pandas(self) -> pd.DataFrame:
        """to_pandas"""
        return self.df

    def describe(self):
        """Generate summary statistics"""
        return self.df.describe()

    def head(self, n: int = 5):
        """head"""
        return self.dl.head(n).to_pandas() if not self._is_df_fresh else self.df.head(n)

    @property
    def values(self):
        """values

        Returns:
            _type_: np.ndarray
        """
        self.refresh_pandas()
        return self.df.values

    @property
    def loc(self): # never inplace
        """loc

        Returns:
            _type_: _description_
        """
        self.refresh_pandas()
        obj = self.copy()

        return DataFrameLocator(obj)

    @property
    def iloc(self): # never inplace
        """iloc

        Returns:
            _type_: _description_
        """
        self.refresh_pandas()
        obj = self.copy()
        return IDataFrameLocator(obj)
