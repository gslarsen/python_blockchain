blockchain = []


def get_last_blockchain_value():
    return blockchain[-1]


def add_value(transaction_amount, last_transaction=[1]):
    blockchain.append([last_transaction, transaction_amount])


tx_amount = 0

while tx_amount != "x":
    tx_amount = input("Your transaction amount (enter x to exit): ").lower()
    if tx_amount == "x":
        break
    tx_amount = float(tx_amount)
    last_transaction = get_last_blockchain_value() if len(blockchain) > 0 else [1]
    add_value(last_transaction=last_transaction, transaction_amount=tx_amount)


print(blockchain)
