blockchain = []


def get_last_blockchain_value():
    return blockchain[-1] if len(blockchain) > 0 else None


def add_transaction(transaction_amount, last_transaction=[1]):
    """Adds a new value and the last transaction to the blockchain.
    Args:
        transaction_amount: The amount to be added.
        last_transaction: The last transaction in the blockchain (default [1])."""
    if last_transaction == None:
        last_transaction = [1]
    blockchain.append([last_transaction, transaction_amount])


def get_transaction_value():
    tx_amount = float(input("Your transaction amount: "))
    return tx_amount


def verify_chain():
    """Verifies the blockchain by checking if each block is valid."""
    for i in range(1, len(blockchain)):
        if blockchain[i][0] != blockchain[i - 1]:
            return False
    return True


waiting_for_input = True

while waiting_for_input:
    print("\nPlease choose:")
    print("\t1: Add a new transaction value")
    print("\t2: Print the blockchain blocks")
    print("\th: Change the last transaction value")
    print("\tq: Quit the program")
    user_choice = input("Your choice: ").lower()

    match user_choice:
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
        case "h":
            # h for hacking the first block - this is just an example
            if len(blockchain) > 1:
                blockchain[0] = [2]
        case "q":
            print("Quitting program...")
            waiting_for_input = False
        case _:  # Default case (like 'default' in other languages)
            print("\nInvalid choice!", end=" ")

    if not verify_chain():
        print("Blockchain is invalid! Exiting...")
        break
