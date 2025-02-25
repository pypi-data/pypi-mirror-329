def deposit(self, amount):
    """
    Deposits the given amount into the account.

    Args:
        amount (float): The amount to deposit.

    Returns:
        float: The updated balance after the deposit.

    Raises:
        ValueError: If the deposit amount is negative.
    """
    # Check if the deposit amount is negative
    if amount < 0:
        raise ValueError("Deposit amount cannot be negative")

    # Update the balance by adding the deposit amount
    self.balance += amount

    # Return the updated balance
    return self.balance