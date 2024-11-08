import pytest
import numpy as np
import polars as pl
from perse import DataFrame

@pytest.fixture
def unified_df():
    np.random.seed(42)
    data = {
        'A': range(10),
        'B': range(10),
        'C': range(10)
    }
    return DataFrame(data)


def test_copy(unified_df):
    df2 = unified_df.copy()
    assert df2.table_name != unified_df.table_name


def test_copy2(unified_df):
    df2 = unified_df.copy()
    df3 = unified_df + df2
    print(df3.shape)


def test_query(unified_df):
    unified_df.query('select B, C from this where A > 5 ')


def test_lock(unified_df):
    a = unified_df.copy()
    unified_df.lock()

    unified_df.loc[unified_df['A'] > 5]  # does not raise but returns with message
    a.unlock()
    b = a.loc[a['A'] > 5]
    assert b.shape != a.shape


def test_iloc(unified_df):
    a = unified_df.copy()

    b = a.iloc[:, [0, 1]]
    assert b.shape != a.shape
