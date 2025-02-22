from dynamic_functioneer.dynamic_decorator import dynamic_function

class BankAccount:
    """
    A simple bank account that supports deposits, withdrawals, and balance inquiries.
    """
    def __init__(self, initial_balance=0.0):
        """
        Initializes the bank account with a starting balance.
        
        Args:
            initial_balance (float): The initial amount in the account.
        """
        self.balance = initial_balance

    @dynamic_function(
        model="meta-llama/llama-3.2-3b-instruct:free",
        extra_info="Deposits a specified amount to the account. Raises an error if the deposit amount is negative.",
        # error_model="meta-llama/llama-3.2-3b-instruct:free"
    )
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
        pass  # Implementation will be dynamically generated.

    @dynamic_function(
        model="meta-llama/llama-3.2-3b-instruct:free",
        extra_info="Withdraws a specified amount from the account. Raises an error if the withdrawal amount is negative or if funds are insufficient.",
        # error_model="meta-llama/llama-3.2-3b-instruct:free"
    )
    def withdraw(self, amount):
        """
        Withdraws the given amount from the account.

        Args:
            amount (float): The amount to withdraw.

        Returns:
            float: The updated balance after the withdrawal.

        Raises:
            ValueError: If the withdrawal amount is negative.
            ValueError: If the account does not have sufficient funds.
        """
        pass  # The decorator will generate the withdrawal logic.

    @dynamic_function(
        model="meta-llama/llama-3.2-3b-instruct:free",
        extra_info="Retrieves the current balance of the account.",
        # error_model="meta-llama/llama-3.2-3b-instruct:free"
    )
    def get_balance(self):
        """
        Returns the current balance of the account.

        Returns:
            float: The current account balance.
        """
        pass  # The dynamic_function decorator will supply this code.

if __name__ == '__main__':
    # Create a bank account with an initial balance of 100.0
    account = BankAccount(100.0)
    print("Initial Balance:", account.get_balance())

    # Deposit an amount and display the updated balance.
    try:
        new_balance = account.deposit(50.0)
        print("Balance after depositing 50.0:", new_balance)
    except Exception as e:
        print("Error during deposit:", e)

    # Withdraw an amount and display the updated balance.
    try:
        new_balance = account.withdraw(30.0)
        print("Balance after withdrawing 30.0:", new_balance)
    except Exception as e:
        print("Error during withdrawal:", e)


