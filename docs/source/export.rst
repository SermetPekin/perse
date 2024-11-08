


Exporting data
------------------------
.. code-block:: python

    from perse import DataFrame
    import numpy as np

    # Generate sample data
    np.random.seed(42)
    data = {
        "A": np.random.randint(0, 100, 10),
        "B": np.random.random(10),
        "C": np.random.choice(["X", "Y", "Z"], 10),
    }

    df = DataFrame(data)

    # Export as CSV file
    df.to_csv('example.csv')

    # Export as Excel file
    df.to_excel('example.xlsx')

    # Export as JSON file
    df.to_json('example.json')




Pipe Operator
================
In Python, the | operator is traditionally used as the OR operator. However, in the DataFrame class, the | operator has been repurposed for a functional, chainable approach, similar to other modern data processing libraries. This enables more readable and flexible expressions.

.. code-block:: python

    # Applying the print function to the DataFrame instance
    df | print

    # Chaining functions: the instance is returned if no modification is made
    df2 = df | print | print

    # Using a lambda function to call `to_csv` with arguments, demonstrating flexibility in piping
    _ = df | (lambda x: x.to_csv('example.csv'))

