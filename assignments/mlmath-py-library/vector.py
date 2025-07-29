def dot_product(a, b):
    """
    Compute the dot product of two vectors.

    Args:
        a (list): First vector.
        b (list): Second vector.

    Returns:
        int or float: Dot product result.

    Example:
        >>> dot_product([1, 2, 3], [4, 5, 6])
        32
    """
    if len(a) != len(b):
        raise ValueError("Vectors must be of same length.")
    return sum(x * y for x, y in zip(a, b))
