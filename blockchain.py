MINING_REWARD = 10.0

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
    # Should open transactions for the recipient also be considered?
    # open_tx_recipient = [
    #     tx["amount"] for tx in open_transactions if tx["recipient"] == participant
    # ]
    # tx_recipient.extend(open_tx_recipient)
    amount_received = sum(tx_recipient)

    return amount_received - amount_sent


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
    if verify_transaction({"sender": sender, "recipient": recipient, "amount": amount}):
        open_transactions.append(
            {"sender": sender, "recipient": recipient, "amount": amount}
        )
        participants.update([sender, recipient])
        return True
    return False


def mine_block():
    """
    1. Mines a new block from open_transactions and adds it to the blockchain
    2. clears open_transactions
    3. returns the new block
    """
    reward_transaction = {
        "sender": "MINING",
        "recipient": owner,
        "amount": MINING_REWARD,
    }
    last_block = blockchain[-1]
    # Convert the previous block's values to a concatenated string
    previous_block_hashed = hash_block(last_block)
    # Create a copy of the transactions
    copied_transactions = open_transactions[:]
    copied_transactions.append(reward_transaction)
    block = {
        "previous_hash": previous_block_hashed,
        "index": len(blockchain),
        "transactions": copied_transactions,
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
                f"**** ERROR! detected at block index:{index} ****\n\tprevious_hash:\n\t{block['previous_hash']} \n\tdoes not match previous block's recalculated_hash:\n\t{recalculated_hash}"
            )
            return False
    return True


def verify_transaction(transaction):
    """Verifies a transaction by checking if it is valid.
    Args:
        transaction: The transaction to be verified.
    """
    sender_balance = get_balance(transaction["sender"])
    return sender_balance >= transaction["amount"]


def verify_transactions():
    """Verifies all transactions in the open_transactions."""
    return all(verify_transaction(tx) for tx in open_transactions)


waiting_for_input = True

while waiting_for_input:
    print("\nPlease choose:")
    print("\t1: Add a new transaction value")
    print("\t2: Mine a new block")
    print("\t3: Print the blockchain blocks")
    print("\t4: Print participants")
    print("\t5: Check transaction validity")
    print("\th: Change the last transaction value")
    print("\tq: Quit the program")
    user_choice = input("Your choice: ").lower()

    match user_choice:
        case "1":
            tx_data = get_transaction_value()
            recipient, amount = tx_data
            print(f"Transaction data: {tx_data}")
            if add_transaction(recipient=recipient, amount=amount):
                print(f"Transaction added: {tx_data}")
            else:
                print(f"**** Transaction failed! Insufficient balance for {owner}.")
            print(f"open_transactions:\n{open_transactions}")
        case "2":
            mined_block = mine_block()
            if mined_block:
                print(f"Block mined: {mined_block}")
                print(f"open_transactions: {open_transactions}")
            else:
                print("**** No transactions to mine! ****")
        case "3":
            if len(blockchain) == 0:
                print("**** No blocks yet! ****")
            else:
                print("The blocks in the blockchain are:")
                for block in blockchain:
                    print(block)
        case "4":
            if len(participants) == 0:
                print("**** No participants yet! ****")
            else:
                print("The participants are:")
                for participant in participants:
                    print(participant)
        case "5":
            if verify_transactions():
                print("All transactions are valid!")
            else:
                print("**** Some transactions are invalid! ****")
        case "h":
            # h for hacking the first block - this is just an example
            if len(blockchain) > 0:
                blockchain[0] = {
                    "previous_hash": "",
                    "index": 1,
                    "transactions": [],
                }
            else:
                print("**** No blocks to hack! ****")
        case "q":
            print("Quitting program...")
            waiting_for_input = False
        case _:  # Default case (like 'default' in other languages)
            print("\n**** Invalid choice! ****", end=" ")

    if not verify_chain():
        print("**** Blockchain is invalid! ****\nExiting...")
        break
    print(f"Balance of {owner}: {get_balance(owner):.2f}")
