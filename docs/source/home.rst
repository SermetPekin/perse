Perse Documentation
===================

Perse is an experimental Python package that merges essential functionalities from **Pandas**, **Polars**, and **DuckDB** into a unified `DataFrame` object. Perse simplifies data handling, manipulation, SQL queries, and visualization by combining features from these powerful libraries.

.. contents::
   :local:

Introduction
------------

Perse combines some of the most-used functions from Pandas, Polars, and DuckDB to provide an efficient and versatile data manipulation experience. This package is currently experimental, with plans to expand its functionality.

Installation
------------

To install Perse, use pip:

.. code-block:: bash

    pip install perse

Getting Started
---------------

Here’s a quick example to get you started with Perse:

.. code-block:: python

    from perse import DataFrame
    import numpy as np
    import polars as pl

    # Sample data generation
    np.random.seed(42)
    data = {
        "A": np.random.randint(0, 100, 10),
        "B": np.random.random(10),
        "C": np.random.choice(["X", "Y", "Z"], 10),
    }


    df = DataFrame(data)
.. code-block:: text

    shape: (10, 3)
    ┌─────┬──────────┬─────┐
    │ A   ┆ B        ┆ C   │
    │ --- ┆ ---      ┆ --- │
    │ i64 ┆ f64      ┆ str │
    ╞═════╪══════════╪═════╡
    │ 51  ┆ 0.866176 ┆ Y   │
    │ 92  ┆ 0.601115 ┆ X   │
    │ 14  ┆ 0.708073 ┆ X   │
    │ 71  ┆ 0.020584 ┆ X   │
    │ 60  ┆ 0.96991  ┆ Z   │
    │ 20  ┆ 0.832443 ┆ Z   │
    │ 82  ┆ 0.212339 ┆ Z   │
    │ 86  ┆ 0.181825 ┆ Y   │
    │ 74  ┆ 0.183405 ┆ Z   │
    │ 74  ┆ 0.304242 ┆ Y   │
    └─────┴──────────┴─────┘


Functionality Overview
----------------------

Data Manipulation
~~~~~~~~~~~~~~~~~

These methods allow for common data manipulations like adding columns, filtering rows, and generating summary statistics. The methods in this group are essential for basic data handling.

**Examples:**

.. code-block:: python

    # Add a new column to the DataFrame
    df.add_column("D", np.random.random(10))

    # Filter rows where column "A" is greater than 50
    df2 = df.filter_rows(df.dl["A"] > 50)

    # Get a summary of the data using Pandas' describe method
    print(df2.describe())

SQL Querying
~~~~~~~~~~~~

Leverage DuckDB to run SQL queries directly on the DataFrame. This feature allows advanced data manipulations using SQL syntax and enables filtering, aggregating, and joining data.

**Example:**

.. code-block:: python

    # Use DuckDB SQL to filter rows
    result = df.query("SELECT * FROM this WHERE A > 50")
    print(result)

Indexing and Selection
~~~~~~~~~~~~~~~~~~~~~~

Provides methods for accessing specific rows or columns using Pandas-like `.loc` and `.iloc` properties. Supports conditions and positional indexing.

**Examples:**

.. code-block:: python

    # Selecting rows where A > 50 using .loc
    df2  = df.loc[df["A"] > 50, :]
    print(df2)

    # Display first few rows of the DataFrame
    print(df2.head(3))

Visualization
~~~~~~~~~~~~~

Create visualizations using Matplotlib. This includes scatter plots, bar charts, and more to help visualize data directly from the Perse DataFrame.

**Examples:**

.. code-block:: python

    # Scatter plot for columns "A" and "B"
    df.plot(
        x="A",
        y="B",
        kind="scatter",
        title="Scatter Plot of A vs B",
        xlabel="A values",
        ylabel="B values",
    )

    # Bar plot for category "C" by values in column "A"
    df.plot(kind="bar", x="C", y="A", title="Bar Plot by Category C")

API Reference
-------------

DataFrame
~~~~~~~~~

The core class in Perse that combines Polars, Pandas, and DuckDB functionality.

Attributes
^^^^^^^^^^

- **df**: Returns the Pandas version of the DataFrame, converting from Polars as needed.
- **dl**: The Polars version of the DataFrame.
- **locked**: Prevents further modifications to the DataFrame until `unlock` is called.

Methods
^^^^^^^

- ``__init__(data)``: Initializes the DataFrame with data from a dictionary, file path, or existing DataFrame.
- ``query(sql)``: Runs SQL on the DataFrame using DuckDB. Use `"this"` in the query to refer to the table.
- ``add_column(name, values)``: Adds a new column to the DataFrame.
- ``filter_rows(condition)``: Filters rows based on a given condition.
- ``lock()``: Locks the DataFrame to prevent modifications.
- ``unlock()``: Unlocks the DataFrame to allow modifications.
- ``plot(kind, x, y)``: Plots data using Matplotlib.

Future Plans
------------

Perse is in early development, with plans to include:

- Advanced SQL querying features.
- More data manipulation functions inspired by Pandas and Polars.
- Enhanced visualization options.

Contributing
------------

Contributions are welcome! If you have ideas or suggestions for improving Perse, please open an issue or submit a pull request.

License
-------

This project is licensed under the MIT License.
