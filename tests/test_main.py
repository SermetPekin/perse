
import pytest
import numpy as np
import pandas as pd
import polars as pl
from perse import DataFrame


@pytest.fixture
def unified_df():
    np.random.seed(42)
    data = {
        'A': np.random.randint(0, 100, 10),
        'B': np.random.random(10),
        'C': np.random.choice(['X', 'Y', 'Z'], 10)
    }
    df_pl = pl.DataFrame(data)
    return DataFrame(dl=df_pl)


def get_dict():
    data = {
        'A': np.random.randint(0, 100, 10),
        'B': np.random.random(10),
        'C': np.random.choice(['X', 'Y', 'Z'], 10)
    }
    return data


def test_creations():
    data = get_dict()
    d1 = pl.DataFrame(data)
    d2 = pl.DataFrame(pd.DataFrame(data))
    d3 = pl.DataFrame(pl.DataFrame(pd.DataFrame(data)))
    assert d1.shape == d2.shape == d3.shape


def test_apply_double():
    data = get_dict()
    d1 = DataFrame(data)
    assert d1

def test_add_column(unified_df):
    new_column_data = np.random.random(10)
    unified_df.add_column('D', new_column_data , inplace=True)

    assert 'D' in unified_df.dl.columns

    df_pandas = unified_df.df
    assert 'D' in df_pandas.columns
    np.testing.assert_array_almost_equal(df_pandas['D'].values, new_column_data)


def test_filter_rows(unified_df):
    condition = unified_df.dl['A'] > 50
    unified_df.filter_rows(condition , inplace=True)

    assert all(unified_df.dl['A'] > 50)

    df_pandas = unified_df.df
    assert all(df_pandas['A'] > 50)


def test_describe(unified_df):
    describe_df = unified_df.describe()
    assert isinstance(describe_df, pd.DataFrame)

    expected_columns = ['A', 'B']
    for col in expected_columns:
        assert col in describe_df.columns


def test_lazy_conversion(unified_df):
    assert not unified_df._is_df_fresh
    _ = unified_df.df
    assert unified_df._is_df_fresh


    unified_df.add_column('E', np.random.random(10) , inplace=True)
    assert not unified_df._is_df_fresh


def test_head(unified_df):
    polars_head = unified_df.dl.head(3).to_pandas()
    pandas_head = unified_df.df.head(3)
    pd.testing.assert_frame_equal(polars_head, pandas_head)
