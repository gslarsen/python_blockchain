genesis_block = {
    "previous_hash": "",  # No previous hash for the genesis block
    "index": 0,
    "transactions": [],
}
blockchain = [genesis_block]
open_transactions = []
owner = "GregoryLarsen"


def hash_block(block):
    """Hashes a block and returns the hash value.
    Args:
        block: The block to be hashed.
    """
    return "-".join([str(val) for val in block.values()])


def get_transaction_value():
    """Returns the transaction amount from the user input."""
    tx_recipient = input("Recipient name: ")
    tx_amount = float(input("Your transaction amount: "))
    return tx_recipient, tx_amount


def add_transaction(recipient, sender=owner, amount=1.0):
    """Adds a new transaction to open_transactions.
    Args:
        sender: sender of the coins.
        recipient: recipient of the coins.
        amount: The amount to be added (default 1.0)."""
    open_transactions.append(
        {"sender": sender, "recipient": recipient, "amount": amount}
    )


def mine_block():
    """
    1. Mines a new block from open_transactions and adds it to the blockchain
    2. clears open_transactions
    3. returns the new block
    """
    last_block = blockchain[-1]
    # Convert the previous block's values to a concatenated string
    previous_block_hashed = hash_block(last_block)
    block = {
        "previous_hash": previous_block_hashed,
        "index": len(blockchain),
        "transactions": open_transactions[:],  # Create a copy of the transactions
    }
    blockchain.append(block)
    open_transactions.clear()
    return block


def verify_chain():
    """Verifies the blockchain by checking if each block is valid."""
    for index in range(1, len(blockchain)):
        block = blockchain[index]
        previous_block = blockchain[index - 1]
        recalculated_hash = hash_block(previous_block)
        if block["previous_hash"] != recalculated_hash:
            print(
                f"ERROR! detected at block index:{index}\n\tprevious_hash: {block['previous_hash']} does not match previous block's recalculated_hash: {recalculated_hash}"
            )
            return False
    return True


waiting_for_input = True

while waiting_for_input:
    print("\nPlease choose:")
    print("\t1: Add a new transaction value")
    print("\t2: Mine a new block")
    print("\t3: Print the blockchain blocks")
    print("\th: Change the last transaction value")
    print("\tq: Quit the program")
    user_choice = input("Your choice: ").lower()

    match user_choice:
        case "1":
            tx_data = get_transaction_value()
            recipient, amount = tx_data
            add_transaction(recipient, amount=amount)
            print(f"open_transactions:\n{open_transactions}")
        case "2":
            mined_block = mine_block()
            if mined_block:
                print(f"Block mined: {mined_block}")
                print(f"open_transactions: {open_transactions}")
            else:
                print("No transactions to mine!")
        case "3":
            if len(blockchain) == 0:
                print("no blocks yet!")
            else:
                print("The blocks in the blockchain are:")
                for block in blockchain:
                    print(block)
        case "h":
            # h for hacking the first block - this is just an example
            if len(blockchain) > 0:
                blockchain[0] = {
                    "previous_hash": "",
                    "index": 1,
                    "transactions": [],
                }
            else:
                print("No blocks to hack!")
        case "q":
            print("Quitting program...")
            waiting_for_input = False
        case _:  # Default case (like 'default' in other languages)
            print("\nInvalid choice!", end=" ")

    if not verify_chain():
        print("Blockchain is invalid! Exiting...")
        break
