def amount_to_int(amount: str) -> int:
    """
    Eg: $ 7.613.726 -> 7613726

    Convert an amount string to an integer.
    """
    return int(amount.replace("$", "").replace(".", "").replace(" ", "").strip())
