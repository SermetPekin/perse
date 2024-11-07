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

from dataclasses import dataclass, field
from typing import Union
import pandas as pd
import polars as pl
import duckdb
import uuid


@dataclass
class BaseDataFrame:
    """BaseDataFrame

    Returns:
        _type_: _description_
    """

    dl: pl.DataFrame = field(default_factory=pl.DataFrame)  # Polars as primary
    _df: pd.DataFrame = field(default_factory=pd.DataFrame, init=False, repr=False)
    _is_df_fresh: bool = field(default=True, init=False, repr=False)
    _duckdb_conn: duckdb.DuckDBPyConnection = field(
        default=None, init=False, repr=False
    )
    _duckdb_initialized: bool = field(default=False, init=False, repr=False)
    table_name: Union[str, None] = None
    locked: bool = False

    @property
    def shape(self):
        """shape"""
        return self.dl.shape

    def __post_init__(self):
        self._is_df_fresh = False
        if isinstance(self.dl, pl.DataFrame):
            ...
        if isinstance(self.dl, pd.DataFrame):
            self.dl = pl.DataFrame(self.dl)
        if isinstance(self.dl, dict):
            self.dl = pl.DataFrame(pd.DataFrame(self.dl))

        _ = self.get_table_name()

    def locked_message(self):
        """locked_message"""
        template = """
        This DataFrame is locked to avoid mistake. 
        In order to unlock use method `unlock`
        e.g.

        df.unlock()

        """
        print(template)
        return self

    def unlocked_message(self):
        """unlocked_message"""
        template = """
        This DataFrame is now unlocked. New values can be added, can be filtered 

        In order to lock use method `lock`
        e.g.

        df.lock()

        """
        print(template)
        return self

    def lock(self):
        """lock"""
        self.locked = True
        return self.locked_message()

    def unlock(self):
        """unlock"""
        self.locked = False
        return self.unlocked_message()

    def __str__(self):
        template = "=========== |colum| DataFrame ===========\n"
        template += str(self.dl)
        return template

    def __repr__(self):
        return self.__str__()

    def __getitem__(self, key):
        """Get column(s) from Polars, converting to Pandas if needed."""
        self.refresh_pandas()
        return self._df[key]

    def __setitem__(self, key, value):
        """Set column(s) in Polars and mark Pandas as 'not fresh'."""
        if self.locked:
            return self.locked_message()

        self.dl = self.dl.with_columns(pl.Series(key, value))
        self._is_df_fresh = False

    def init_duck(self):
        """Initialize the DuckDB connection if not already initialized."""
        if not self._duckdb_initialized:
            self._duckdb_conn = duckdb.connect()
            self._duckdb_initialized = True

    def get_table_name(self) -> str:
        """Generate or retrieve a unique table name for the DuckDB connection."""
        if not hasattr(self, "table_name") or not isinstance(self.table_name, str):
            self.table_name = f"temp_{uuid.uuid4().hex}"
        return self.table_name

    def sql_to_polars(self, query: str) -> pl.DataFrame:
        """Execute SQL and return result as Polars DataFrame."""
        result_df = self.execute_sql(query)
        return result_df.dl

    def sql_to_pandas(self, query: str) -> pd.DataFrame:
        """Execute SQL and return result as Pandas DataFrame."""
        return self.execute_sql(query).df

    def __add__(self, other):
        """Concatenate two DataFrames based on shape and columns."""

        if not isinstance(other, BaseDataFrame):
            raise TypeError("Can only add another DataFrame instance.")

        if self.locked:
            return self.locked_message()

        self.refresh_pandas()
        other.refresh_pandas()

        if set(self.df.columns) == set(other.df.columns):
            combined_df = pd.concat([self.df, other.df], ignore_index=True)
        else:
            combined_df = pd.concat(
                [self.df, other.df], axis=0, ignore_index=True, join="outer"
            )

        return self.final_init(dl=pl.DataFrame(combined_df))
