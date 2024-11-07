[![Python Package](https://github.com/SermetPekin/perse/actions/workflows/python-package.yml/badge.svg)](https://github.com/SermetPekin/perse/actions/workflows/python-package.yml)[![PyPI](https://img.shields.io/pypi/v/perse)](https://img.shields.io/pypi/v/perse)[![Supported Python Versions](https://img.shields.io/pypi/pyversions/perse)](https://pypi.org/project/perse/) 





# Perse

**Perse** is an experimental Python package that combines some of the most widely-used functionalities from the powerhouse libraries **Pandas**, **Polars**, and **DuckDB** into a single, unified `DataFrame` object. The goal of Perse is to provide a streamlined and efficient interface, leveraging the strengths of these libraries to create a versatile data handling experience.

This package is currently experimental, with a focus on essential functions. We plan to expand its capabilities by integrating more features from Pandas, Polars, and DuckDB in future versions.

## Key Features

The `Perse` DataFrame currently supports the following functionalities:

### 1. Data Manipulation
Core data-handling tools inspired by Pandas and Polars.

- **Indexing and Selection**: Access specific rows or columns with `.loc` and `.iloc` properties.
- **Column Operations**: Add, modify, or delete columns efficiently.
- **Row Filtering**: Filter rows based on specific conditions.
- **Aggregation**: Summarize data with aggregations like `sum`, `mean`, `count`.
- **Sorting**: Sort data based on column values.
- **Custom Function Application**: Apply custom functions to columns, supporting both element-wise operations and complex transformations.

### 2. SQL Querying
Use DuckDB's SQL engine to run SQL queries directly on the DataFrame, ideal for complex filtering and data manipulation.

- **Direct SQL Queries**: Run SQL queries directly on data using DuckDB’s powerful engine.
- **Seamless Integration**: Convert between Polars and DuckDB seamlessly for efficient querying on large datasets.
- **Advanced Filtering**: Filter, join, and group data using SQL syntax.

### 3. Data Transformation
A collection of versatile data transformation functions.

- **Pivot and Unpivot**: Reshape data for summary reports and visualizations.
- **Melt/Stack**: Transform data between wide and long formats.
- **Mapping and Replacing**: Map values based on conditions or replace them in columns.
- **Grouping and Window Functions**: Group by specific columns and apply aggregations or window functions for advanced data summarization.

### 4. Compatibility and Conversion
Interoperability between Pandas, Polars, and DuckDB formats, offering flexibility in data manipulation.

- **Pandas Compatibility**: Conversion utilities to easily move data between Pandas and Polars.
- **Automatic Data Handling**: Automatically convert and handle data depending on the operation, allowing users to work flexibly with either Pandas or Polars.
- **File I/O Support**: Read and write from common file formats (e.g., CSV, Parquet, JSON).

### 5. Visualization
Basic plotting capabilities that make it easy to visualize data directly from the Perse DataFrame.

- **Line, Bar, and Scatter Plots**: Quick visualizations with common plot types.
- **Customization**: Customize plot titles, labels, and legends with Matplotlib.
- **Direct Plotting**: Plot directly from the Perse DataFrame, which internally uses Pandas’ Matplotlib integration.

### 6. Data Integrity and Locking
Features designed to prevent accidental modifications and ensure data integrity.

- **Locking Mechanism**: Lock the DataFrame to prevent accidental edits.
- **Unlocking**: Explicitly unlock to allow modifications.
- **Validation**: Ensure data type consistency across columns for critical operations.

## Installation

To install Perse, run:

```bash
pip install perse
```
### Usage 

```python 


from perse import DataFrame
import numpy as np
import polars as pl

# Sample data creation
data = {"A": [1, 2, 3], "B": [0.5, 0.75, 0.86], "C": ["X", "Y", "Z"]}
df = DataFrame(data)

# Apply SQL query
result = df.query("SELECT * FROM this WHERE B < 0.86")
print(result.df)

# Add a new column with custom transformation
df.add_column("D", [10, 20, 30])
print("After adding column D:")
print(df.df)

# Filter rows
df.filter_rows(df.dl["A"] > 50)
print("Filtered DataFrame where A > 50:")
print(df.df)

# Lock and unlock the DataFrame
df.lock()
print("DataFrame is now locked.")
df.unlock()
print("DataFrame is now unlocked and editable.")

# Plot data
df.plot(kind="bar", x="A", y="B", title="Sample Bar Plot")



```


### Examples 

```python 

from perse import DataFrame
import numpy as np
import polars as pl

# Sample data
data = {"A": np.random.randint(0, 100, 10), "B": np.random.random(10), "C": np.random.choice(["X", "Y", "Z"], 10)}
df = DataFrame(dl=pl.DataFrame(data))

# 1. Add a New Column
df.add_column("D", np.random.random(10))
print("DataFrame with new column D:\n", df.df)

# 2. Filter Rows
df.filter_rows(df.dl["A"] > 50)
print("Filtered DataFrame (A > 50):\n", df.df)

# 3. SQL Querying with DuckDB
result = df.query("SELECT A, AVG(B) AS avg_B FROM this GROUP BY A")
print("SQL Query Result:\n", result.df)

# 4. Visualization
df.plot(kind="scatter", x="A", y="B", title="Scatter Plot of A vs B", xlabel="A values", ylabel="B values")

# 5. Convert to Pandas
pandas_df = df.to_pandas()
print("Converted to Pandas DataFrame:\n", pandas_df)


```
