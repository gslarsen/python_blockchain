blockchain = []


def get_last_blockchain_value():
    return blockchain[-1] if len(blockchain) > 0 else None


def add_transaction(transaction_amount, last_transaction=[1]):
    """Adds a new value to the blockchain, as well as the last transaction.
    Args:
        transaction_amount: The amount to be added.
        last_transaction: The last transaction in the blockchain (default [1])."""
    if last_transaction == None:
        last_transaction = [1]
    blockchain.append([last_transaction, transaction_amount])


def get_transaction_value():
    tx_amount = float(input("Your transaction amount: "))
    return tx_amount


while True:
    print("\nPlease choose:")
    print("\t1: Add a new transaction value")
    print("\t2: Print the blockchain blocks")
    print("\tq: Quit the program")
    user_choice = input("Your choice (1 or 2, enter q to exit): ").lower()

    match user_choice:
        case "q":
            print("Quitting program...")
            break
        case "1":
            tx_amount = get_transaction_value()
            last_transaction = get_last_blockchain_value()
            add_transaction(tx_amount, last_transaction)
        case "2":
            if len(blockchain) == 0:
                print("no blocks yet!")
            else:
                print("The blocks in the blockchain are:")
                for block in blockchain:
                    print(block)
        case _:  # Default case (like 'default' in other languages)
            print("\nInvalid choice!", end=" ")
