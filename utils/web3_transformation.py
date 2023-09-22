from web3 import Web3
from eth_account import Account
from eth_account.messages import encode_defunct
from web3 import Web3
from decouple import config


def transfer_to_keccak256(data_for_hash):
    infura_url = config("INFURA_URL")
    w3 = Web3(Web3.HTTPProvider(infura_url))
    data_bytes = Web3.to_bytes(text=str(data_for_hash))
    hash_bytes = Web3.keccak(data_bytes)
    hash_hex = Web3.to_hex(hash_bytes)
    print(len(hash_hex))

    return hash_hex


def transfer_to_signed_message(hash_hex):
    hashed_data_bytes = Web3.to_bytes(hexstr=hash_hex)
    message_prefix = "\x19Ethereum Signed Message:\n"
    message_length = len(hashed_data_bytes)

    message_length_bytes = bytes(str(message_length), 'utf-8')

    message = message_prefix.encode() + message_length_bytes + hashed_data_bytes

    final_hash = Web3.keccak(message)
    final_hash_hex = final_hash.hex()
    return final_hash_hex


def signing_private_key(date):
    message = encode_defunct(text=date)
    private_key = config("PRIVATEKEY")
    account = Account.from_key(private_key)
    signed_message = account.sign_message(message)
    signature = signed_message.signature.hex()
    return signature

