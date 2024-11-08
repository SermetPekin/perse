
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

