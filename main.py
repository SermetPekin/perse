from perse import DataFrame
import polars as pl
import numpy as np


def first():
    # Sample data generation
    np.random.seed(42)
    data = {
        "A": np.random.randint(0, 100, 10),
        "B": np.random.random(10),
        "C": np.random.choice(["X", "Y", "Z"], 10),
    }

    # Initialize UnifiedDataFrame with Polars DataFrame
    df_pl = pl.DataFrame(data)
    unified_df = DataFrame(dl=df_pl)

    # Example: Add a new column
    print("Original Polars DataFrame:")
    print(unified_df.dl)

    unified_df.add_column("D", np.random.random(10))
    print("\nPolars DataFrame after adding a column:")
    print(unified_df.dl)

    print("\nPandas DataFrame after adding a column (on-demand conversion):")
    print(unified_df.df)  # Should reflect the new column 'D'

    # Example: Filter rows
    unified_df.filter_rows(unified_df.dl["A"] > 50)
    print("\nPolars DataFrame after filtering rows where A > 50:")
    print(unified_df.dl)

    print("\nPandas DataFrame after filtering (on-demand conversion):")
    print(unified_df.df)

    # Example: Describe the data (requires Pandas)
    print("\nSummary statistics using Pandas' describe method:")
    print(unified_df.describe())

    # Example: Head operation
    print("\nFirst 3 rows in both Polars and Pandas:")
    print("Polars Head:")
    print(unified_df.dl.head(3))
    print("\nPandas Head (after conversion):")
    print(unified_df.df.head(3))


    d = unified_df.loc[unified_df["A"] > 50, :]
    print(d)


    # Plot a line plot for column 'A' and 'B'
    unified_df.plot(
        x="A",
        y="B",
        kind="scatter",
        title="Scatter Plot of A vs B",
        xlabel="A values",
        ylabel="B values",
    )

    # You can also create other types of plots
    unified_df.plot(kind="bar", x="C", y="A", title="Bar Plot by Category C")


def duck():
    
    # Initialize DataFrame with random data in Polars format
    import numpy as np

    np.random.seed(42)
    data = {
        'A': np.random.randint(0, 100, 10),
        'B': np.random.random(10),
        'C': np.random.choice(['X', 'Y', 'Z'], 10)
    }
    unified_df = DataFrame(dl=pl.DataFrame(data))
    # unified_df2 = DataFrame(dl=pl.DataFrame(data))

    # DuckDB functionality is not initialized until required
    print("Using DuckDB SQL for filtering:")
    query_result = unified_df.sql_to_pandas("SELECT * FROM this WHERE A > 50")
    print(query_result)

    # Save to DuckDB (initializes DuckDB if not yet done)
    unified_df.save_to_duckdb("my_table")

    # Load data back from DuckDB (uses existing DuckDB connection)
    unified_df.load_from_duckdb("my_table")
    print("\nLoaded from DuckDB:")
    print(unified_df.df)

duck()