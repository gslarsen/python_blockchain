genesis_block = {
    "previous_hash": "",  # No previous hash for the genesis block
    "index": 0,
    "transactions": [],
}
blockchain = [genesis_block]
open_transactions = []
owner = "GregoryLarsen"
participants = {owner}


def hash_block(block):
    """Hashes a block and returns the hash value.
    Args:
        block: The block to be hashed.
    """
    return "-".join([str(val) for val in block.values()])


def get_balance(participant):
    """Calculates and returns the balance of a participant.
    Args:
        participant: The participant whose balance is to be calculated.
    """
    tx_sender = [
        tx["amount"]
        for block in blockchain
        for tx in block["transactions"]
        if tx["sender"] == participant
    ]
    open_tx_sender = [
        tx["amount"] for tx in open_transactions if tx["sender"] == participant
    ]
    tx_sender.extend(open_tx_sender)
    amount_sent = sum(tx_sender)

    tx_recipient = [
        tx["amount"]
        for block in blockchain
        for tx in block["transactions"]
        if tx["recipient"] == participant
    ]
    open_tx_recipient = [
        tx["amount"] for tx in open_transactions if tx["recipient"] == participant
    ]
    tx_recipient.extend(open_tx_recipient)
    amount_received = sum(tx_recipient)

    return amount_received - amount_sent


def get_transaction_value():
    """Returns the transaction amount from the user input."""
    tx_sender = input("Your name: ")
    tx_recipient = input("Recipient name: ")
    tx_amount = float(input("Your transaction amount: "))
    return tx_sender, tx_recipient, tx_amount


def add_transaction(recipient, sender=owner, amount=1.0):
    """Adds a new transaction to open_transactions.
    Args:
        sender: sender of the coins.
        recipient: recipient of the coins.
        amount: The amount to be added (default 1.0)."""
    open_transactions.append(
        {"sender": sender, "recipient": recipient, "amount": amount}
    )
    participants.update([sender, recipient])


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
    print("\t4: Print participants")
    print("\th: Change the last transaction value")
    print("\tq: Quit the program")
    user_choice = input("Your choice: ").lower()

    match user_choice:
        case "1":
            tx_data = get_transaction_value()
            print(f"Transaction data: {tx_data}")
            sender, recipient, amount = tx_data
            add_transaction(recipient=recipient, sender=sender, amount=amount)
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
        case "4":
            if len(participants) == 0:
                print("No participants yet!")
            else:
                print("The participants are:")
                for participant in participants:
                    print(participant)
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
    print(f"Balance of {owner}: {get_balance(owner)}")
