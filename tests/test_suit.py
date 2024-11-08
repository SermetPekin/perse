import pytest
import polars as pl
import pandas as pd
import numpy as np
from perse import DataFrame


@pytest.fixture
def sample_data():
    data = {
        "A": np.random.randint(0, 100, 10),
        "B": np.random.random(10),
        "C": np.random.choice(["X", "Y", "Z"], 10),
    }
    return DataFrame(dl=pl.DataFrame(data))


def test_add_column(sample_data):
    sample_data.add_column("D", np.random.random(10), inplace=True)
    assert "D" in sample_data.dl.columns
    assert len(sample_data.dl["D"]) == 10


def test_filter_rows(sample_data):
    initial_count = len(sample_data.dl)
    sample_data.filter_rows(sample_data.dl["A"] > 50, inplace=True)
    assert len(sample_data.dl) <= initial_count
    assert all(sample_data.dl["A"] > 50)


def test_to_pandas(sample_data):
    pandas_df = sample_data.to_pandas()
    assert isinstance(pandas_df, pd.DataFrame)
    assert pandas_df.shape == sample_data.dl.shape


def test_describe(sample_data):
    description = sample_data.describe()
    assert isinstance(description, pd.DataFrame)
    assert "A" in description.columns
    assert "B" in description.columns


def test_head(sample_data):
    head_df = sample_data.head(3)
    assert len(head_df) == 3
    assert isinstance(head_df, pd.DataFrame)


def test_loc_iloc(sample_data):
    sample_data.df["A"] = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    loc_df = sample_data.loc[sample_data.df["A"] > 50]
    assert loc_df.shape[0] == 5  # 5 values should be greater than 50

    iloc_value = sample_data.iloc[0, 1]
    assert isinstance(iloc_value, float)


def test_plot(sample_data):
    import matplotlib.axes

    ax = sample_data.plot(kind="line", x="A", y="B", show=False)
    assert isinstance(ax, matplotlib.axes.Axes)


def test_duckdb_execute_sql(sample_data):
    query = "SELECT A, AVG(B) AS avg_B FROM this GROUP BY A"
    result_df = sample_data.execute_sql(query)
    assert isinstance(result_df, DataFrame)
    assert "A" in result_df.dl.columns
    assert "avg_B" in result_df.dl.columns


def test_sql_to_polars(sample_data):
    query = "SELECT A, COUNT(*) AS count_A FROM this GROUP BY A"
    result_df = sample_data.sql_to_polars(query)
    assert isinstance(result_df, pl.DataFrame)
    assert "A" in result_df.columns
    assert "count_A" in result_df.columns


def test_sql_to_pandas(sample_data):
    query = "SELECT A, MAX(B) AS max_B FROM this GROUP BY A"
    result_df = sample_data.sql_to_pandas(query)
    assert isinstance(result_df, pd.DataFrame)
    assert "A" in result_df.columns
    assert "max_B" in result_df.columns


def test_save_to_duckdb(sample_data):
    sample_data.save_to_duckdb("test_table")
    result = sample_data.sql_to_pandas("SELECT * FROM test_table")
    assert isinstance(result, pd.DataFrame)
    assert set(result.columns) == set(sample_data.dl.columns)


def test_load_from_duckdb(sample_data):
    sample_data.save_to_duckdb("test_table_load")
    sample_data.load_from_duckdb("test_table_load")
    assert isinstance(sample_data.df, pd.DataFrame)
    assert sample_data.df.shape == sample_data.dl.shape
