from perse import DataFrame


def get_dict():
    return {'A': range(10), 'B': range(10)}


def test_inplace():
    data = get_dict()
    df = DataFrame(data)
    df2 = df.add_column('C', range(10))
    assert df.shape == (10, 2)
    assert df2.shape == (10, 3) and 'C' in df2.df.columns

    assert 'C' in df2
    assert 'C' not in df


def test_inplace2():
    data = get_dict()
    df = DataFrame(data)
    df2 = df.add_column('C', range(10))
    dfA = df2.loc[:, ['A']]
    assert df.shape == (10, 2)
    assert df2.shape == (10, 3) and 'C' in df2.df.columns
    assert 'C' in df2
    assert dfA.shape == (10, 1)

    df3 = df.query('select * from this where A < 5 ')
    assert df.shape == (10, 2)
    assert df3.shape == (5, 2)
