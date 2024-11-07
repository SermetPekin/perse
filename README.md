[![Python Package](https://github.com/SermetPekin/perse/actions/workflows/python-package.yml/badge.svg)](https://github.com/SermetPekin/perse/actions/workflows/python-package.yml)

[![PyPI](https://img.shields.io/pypi/v/perse)](https://img.shields.io/pypi/v/perse) 
[![Supported Python Versions](https://img.shields.io/pypi/pyversions/perse)](https://pypi.org/project/perse/) 
[![Downloads](https://static.pepy.tech/badge/perse)](https://pepy.tech/project/perse) 


[![Downloads](https://static.pepy.tech/badge/perse/month)](https://pepy.tech/project/perse)
[![Downloads](https://pepy.tech/badge/perse/week)](https://pepy.tech/project/perse)
[![Python Package](https://github.com/SermetPekin/perse-private/actions/workflows/python-package.yml/badge.svg)](https://github.com/SermetPekin/perse-private/actions/workflows/python-package.yml)




# Perse

**Perse** is an experimental Python package that combines some of the most widely-used functionalities from the powerhouse libraries **Pandas**, **Polars**, and **DuckDB** into a single, unified `DataFrame` object. The goal of Perse is to provide a streamlined and efficient interface, leveraging the strengths of these libraries to create a versatile data handling experience.

This package is currently experimental, with a focus on essential functions. We plan to expand its capabilities by integrating more features from Pandas, Polars, and DuckDB in future versions.

## Key Features

The `Perse` DataFrame currently supports the following functionalities:

- **Data Manipulation**:
  - Row and column indexing using Pandas-style `.loc` and `.iloc` properties.
  - Addition of new columns and basic row/column filtering.
  - Application of custom functions to columns with support for both element-wise operations and complex transformations.

- **SQL Querying**:
  - Leverage DuckDB's SQL engine to run SQL queries directly on the DataFrame, allowing for advanced data manipulations and filtering with SQL syntax.
  - Seamless conversion between Polars and DuckDB to enable efficient querying on large datasets.

- **Visualization**:
  - Basic plotting capabilities using Matplotlib. Supports line, bar, scatter plots, and more, making it easy to visualize data directly from the Perse DataFrame.

- **Compatibility**:
  - Conversion utilities between Pandas and Polars DataFrames, making it easy to work in both environments.
  - Automatic handling of data in either Pandas or Polars formats depending on the operation, offering flexibility in data manipulation.

## Installation

To install Perse, run:

```bash
pip install perse 
```


```python 
from perse import DataFrame

# Create a sample DataFrame
data = {"A": [1, 2, 3], "B": [0.5, 0.75, 0.86]}
df = DataFrame(data)

# Apply SQL query
result = df.query("SELECT * FROM this WHERE B < 0.86")
print(result.df)

# Add a new column with custom transformation
df.add_column("C", [10, 20, 30])
print("After adding column C:")
print(df.df)

# Lock and unlock the DataFrame
df.lock()
print("DataFrame is now locked.")
df.unlock()
print("DataFrame is now unlocked and editable.")

# Plot data
df.plot(kind="bar", x="A", y="B")

```
