# this module implements a simple blockchain with basic transaction handling
from collections import OrderedDict
import json

# import pickle

from hash_util import hash_block, hash_string_sha256

# this print statement will only execute if this module is imported, not when run directly
if __name__ != "__main__":
    print("Running module:", __name__)

MINING_REWARD = 10.0

blockchain = []
open_transactions = []
owner = "GregoryLarsen"
participants = {owner}
file_to_save = Path(__file__).with_name("blockchain.txt")


def load_data():
    """Loads the blockchain and open transactions from a file."""
    global blockchain
    global open_transactions
    global participants
    try:
        with open(file_to_save, mode="r") as f:
            # region: Alternative load method using pickle
            # data = pickle.load(f)  # binary safe
            # blockchain = data.get("chain", [genesis_block])
            # open_transactions = data.get("ot", [])
            # participants = set(data.get("participants", [owner]))
            # print("Data loaded.")
            # endregion
            blockchain = json.loads(f.readline())
            blockchain = [
                {
                    "previous_hash": block["previous_hash"],
                    "index": block["index"],
                    "transactions": [
                        OrderedDict(
                            sender=tx["sender"],
                            recipient=tx["recipient"],
                            amount=tx["amount"],
                        )
                        for tx in block["transactions"]
                    ],
                    "proof": block["proof"],
                }
                for block in blockchain
            ]
            print("Blockchain loaded...")
            open_transactions = json.loads(f.readline())
            open_transactions = [
                OrderedDict(
                    sender=tx["sender"], recipient=tx["recipient"], amount=tx["amount"]
                )
                for tx in open_transactions
            ]
            print("Open transactions loaded...")
            participants = set(json.loads(f.readline()))
            print("Participants loaded...")
    except FileNotFoundError:
        print("File not found. Starting with a new blockchain.")
        genesis_block = {
            "previous_hash": "",  # No previous hash for the genesis block
            "index": 0,
            "transactions": [],
            "proof": 100,  # Proof of work for the genesis block
        }
        blockchain = [genesis_block]
    # region: Alternative load method using pickle
    # except (pickle.UnpicklingError, EOFError) as e:
    #     print(f"Corrupt or incompatible pickle file ({e}). Starting fresh.")
    # endregion
    except json.JSONDecodeError as e:
        print(
            f"!file is empty or contains value that is not valid JSON!:\n{type(e).__name__}({e})"
        )
    except Exception as e:
        print(f"!Error loading data!: {type(e).__name__}({e})")
    finally:
        print("\ncleanup load_data completed.")


# Load existing data if available
load_data()


def save_data():
    """Saves the blockchain and open transactions to a file."""
    try:
        with open(file_to_save, mode="w") as f:
            f.write(json.dumps(blockchain) + "\n")
            f.write(json.dumps(open_transactions) + "\n")
            f.write(json.dumps(list(participants)))
            # region: Alternative save method using pickle
            # save_data = {
            #     "chain": blockchain,
            #     "ot": open_transactions,
            #     "participants": list(participants),
            # }
            # f.write(pickle.dumps(save_data))
            # endregion
    except (IOError, OSError) as e:
        print(f"!Error saving data!: {type(e).__name__}({e})")


def valid_proof(transactions, last_hash, proof):
    """Checks if the proof of work is valid.
    Args:
        transactions: The list of transactions in the block.
        last_hash: The hash of the previous block.
        proof: The proof of work to be validated.
    Returns:
        True if the proof is valid, False otherwise."""

    guess = f"{transactions}{last_hash}{proof}".encode()
    guess_hash = hash_string_sha256(guess)
    return guess_hash[:2] == "00"


def proof_of_work():
    """Generates a proof of work for the current block.
    Returns:
        A valid proof of work."""
    last_block = blockchain[-1]
    last_hash = hash_block(last_block)
    proof = 0
    while not valid_proof(open_transactions, last_hash, proof):
        proof += 1
    return proof


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
    # region: Uncomment the following lines if you want to consider open transactions for the recipient
    # Should open transactions for the recipient also be considered?
    # open_tx_recipient = [
    #     tx["amount"] for tx in open_transactions if tx["recipient"] == participant
    # ]
    # tx_recipient.extend(open_tx_recipient)
    # endregion
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
    transaction = OrderedDict(sender=sender, recipient=recipient, amount=amount)
    if verify_transaction(transaction):
        open_transactions.append(transaction)
        participants.update([sender, recipient])
        save_data()
        return True
    return False


def mine_block():
    """
    1. Mines a new block from open_transactions and adds it to the blockchain
    2. clears open_transactions
    3. returns the new block
    """
    last_block = blockchain[-1]
    # Convert the previous block's values to a concatenated string
    previous_block_hashed = hash_block(last_block)
    proof = proof_of_work()
    # Create a reward transaction for the miner
    reward_transaction = OrderedDict(
        sender="MINING",
        recipient=owner,
        amount=MINING_REWARD,
    )
    # region: Create a copy of the open_transactions to avoid modifying the original list
    # This is important to ensure that the original open_transactions list remains unchanged
    # until the block is successfully mined and added to the blockchain
    # endregion
    copied_transactions = open_transactions[:]
    copied_transactions.append(reward_transaction)
    block = {
        "previous_hash": previous_block_hashed,
        "index": len(blockchain),
        "transactions": copied_transactions,
        "proof": proof,
    }

    blockchain.append(block)
    open_transactions.clear()
    save_data()
    return block


def verify_chain():
    """Verifies the blockchain by checking if each block is valid."""
    for index in range(1, len(blockchain)):
        block = blockchain[index]
        previous_block = blockchain[index - 1]
        recalculated_hash = hash_block(previous_block)
        if block["previous_hash"] != recalculated_hash:
            print(
                f"**** ERROR! detected at block index:{index} ****\n\tprevious_hash:\n\t{block['previous_hash']} DOES NOT MATCH  previous block's\n\trecalculated_hash:\n\t{recalculated_hash}"
            )
            return False
        if not valid_proof(
            block["transactions"][:-1], block["previous_hash"], block["proof"]
        ):
            print(
                f"**** ERROR! detected at block index:{index} ****\n\tBlock's proof:\n\t{block['proof']}\n\tBlock's transactions:\n\t{block['transactions']}"
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
                print(f"Transaction added successfully.")
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
                for idx, block in enumerate(blockchain, start=1):
                    print(f"{idx}: {block}")
        case "4":
            if len(participants) == 0:
                print("**** No participants yet! ****")
            else:
                print("The participants are:")
                for participant in participants:
                    print(participant)
                print()
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
    print(f"\nBalance of {owner}: {get_balance(owner):.2f}")
