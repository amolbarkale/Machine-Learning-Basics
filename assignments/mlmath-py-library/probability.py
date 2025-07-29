def conditional_probability(events):
    """
    Compute conditional probability: P(A|B) = P(A and B) / P(B)

    Args:
        events (dict): Dictionary with keys 'A_and_B' and 'B', both values in [0,1]

    Returns:
        float: P(A|B)

    Example:
        >>> conditional_probability({'A_and_B': 0.12, 'B': 0.3})
        0.4
    """
    P_AB = events.get('A_and_B')
    P_B = events.get('B')

    if P_B == 0:
        raise ZeroDivisionError("P(B) cannot be zero.")
    if P_AB is None or P_B is None:
        raise ValueError("Missing keys in events. Required: 'A_and_B' and 'B'.")

    return P_AB / P_B
