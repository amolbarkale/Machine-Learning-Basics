def matrix_multiply(A, B):
    """
    Multiply two matrices using nested loops.

    Args:
        A (list of lists): Matrix A (m x n)
        B (list of lists): Matrix B (n x p)

    Returns:
        list of lists: Resultant matrix (m x p)

    Example:
        >>> A = [[1, 2], [3, 4]]
        >>> B = [[5, 6], [7, 8]]
        >>> matrix_multiply(A, B)
        [[19, 22], [43, 50]]
    """
    if len(A[0]) != len(B):
        raise ValueError("Columns of A must match rows of B.")

    result = []
    for i in range(len(A)):
        row = []
        for j in range(len(B[0])):
            val = sum(A[i][k] * B[k][j] for k in range(len(B)))
            row.append(val)
        result.append(row)
    return result
