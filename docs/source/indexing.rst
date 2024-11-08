Indexing and Filtering
------------------------

The DataFrame class in this package provides powerful indexing and filtering capabilities while ensuring data integrity. By default, all operations return a deep copy, leaving the original instance unchanged. This prevents accidental modifications and ensures that transformations do not alter the original data unless specified.
Key Concepts

- Deep Copy: The DataFrame class always returns a deep copy of itself by default. This preserves the original data, helping to avoid unintended changes.
- inplace Parameter: If you want to modify the data directly without creating a copy, set inplace=True in relevant methods. This allows the original instance to be updated.


.. code-block:: python

    from perse import DataFrame
    import numpy as np

    # Sample data generation
    np.random.seed(42)
    data = {
        "A": np.random.randint(0, 100, 10),
        "B": np.random.random(10),
        "C": np.random.choice(["X", "Y", "Z"], 10),
    }

    df = DataFrame(data)
    original_df = DataFrame(data)

    # Filtering with a deep copy (default)
    df2 = df.filter_rows(df.dl["A"] > 50)

    # Alternatively, modifying the DataFrame in place
    df3 = df.copy()
    df3.filter_rows(df3.dl["A"] > 50, inplace=True)
    assert df2.shape == df3.shape
    assert df.shape == original_df.shape  # Original remains unchanged

    # Pandas-style filtering
    # Creates a deep copy, leaving `df` unchanged
    df4 = df[df["A"] > 50]
    assert df4.shape == df3.shape
    assert df.shape == original_df.shape
