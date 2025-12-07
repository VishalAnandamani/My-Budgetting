def calculate_owed(amount: float, payer: str, spender: str) -> float:
    """
    Calculates how much is owed based on the business logic.

    Logic:
    - If Payer == Spender: Amount Owed = 0 (Paid for self)
    - If Spender == "Shared": Amount Owed = Amount / 2 (Split cost)
    - If Payer != Spender (and not Shared): Amount Owed = Full Amount (Paid for other)

    Returns:
        float: The amount owed by the OTHER person to the PAYER.
    """
    if spender == "Shared":
        return amount / 2.0

    if payer == spender:
        return 0.0

    # If payer != spender and not shared, it means payer paid for spender entirely.
    return float(amount)
