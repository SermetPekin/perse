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
import polars as pl


class SQLDataFrame(BaseDataFrame):
    """"""
    def query(self, query: str):
        """
        Execute a SQL query on the current DataFrame using DuckDB.

        Parameters:
            query (str): The SQL query to execute.

        Returns:
            DataFrame: A new DataFrame instance containing the result of the query.
        """
        return self.execute_sql(query)
    def execute_sql(self, query: str)  : #'DataFrame'
        """
        Execute a SQL query on the current DataFrame using DuckDB.

        Parameters:
            query (str): The SQL query to execute.

        Returns:
            DataFrame: A new DataFrame instance containing the result of the query.
        """
        self.init_duck()
        table_name = self.get_table_name()
        self._duckdb_conn.register(table_name, self.dl.to_pandas())

        query = query.replace("this", table_name)
        result = self._duckdb_conn.execute(query).fetchdf()
        self._duckdb_conn.unregister(table_name)
        return self.final_init(dl=pl.DataFrame(result))

    def save_to_duckdb(self, table_name: str):
        """Save the current DataFrame to a DuckDB table."""
        self.init_duck()
        temp_table = self.get_table_name()
        self._duckdb_conn.register(temp_table, self.dl.to_pandas())
        self._duckdb_conn.execute(
            f"CREATE OR REPLACE TABLE {table_name} AS SELECT * FROM {temp_table}"
        )
        self._duckdb_conn.unregister(temp_table)

    def load_from_duckdb(self, table_name: str):
        """Load data from a DuckDB table into both Pandas and Polars DataFrames."""
        self.init_duck()
        query = f"SELECT * FROM {table_name}"
        result = self._duckdb_conn.execute(query).fetchdf()
        self._df = result
        self.dl = pl.from_pandas(result)
        self._is_df_fresh = True
