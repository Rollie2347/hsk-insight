from web3 import Web3
from typing import Optional
import os

HASHKEY_RPC = os.getenv("HASHKEY_RPC_URL", "https://mainnet.hskchain.com")
HASHKEY_TESTNET_RPC = os.getenv("HASHKEY_TESTNET_RPC_URL", "https://hashkeychain-testnet.alt.technology")

def get_web3(testnet: bool = False) -> Web3:
    rpc = HASHKEY_TESTNET_RPC if testnet else HASHKEY_RPC
    return Web3(Web3.HTTPProvider(rpc))

def get_wallet_data(address: str, testnet: bool = False) -> dict:
    """Fetch wallet balance, tx count, and recent transactions."""
    w3 = get_web3(testnet)
    
    if not w3.is_connected():
        raise ConnectionError("Could not connect to HashKey Chain RPC")
    
    checksum_address = w3.to_checksum_address(address)
    
    balance_wei = w3.eth.get_balance(checksum_address)
    balance_hsk = w3.from_wei(balance_wei, "ether")
    tx_count = w3.eth.get_transaction_count(checksum_address)
    block_number = w3.eth.block_number
    
    # Fetch last 10 blocks of txs involving this address
    recent_txs = []
    scan_blocks = min(50, block_number)
    for i in range(block_number, block_number - scan_blocks, -1):
        if len(recent_txs) >= 10:
            break
        try:
            block = w3.eth.get_block(i, full_transactions=True)
            for tx in block.transactions:
                if tx.get("from", "").lower() == address.lower() or \
                   tx.get("to", "").lower() == address.lower():
                    recent_txs.append({
                        "hash": tx["hash"].hex(),
                        "from": tx["from"],
                        "to": tx.get("to", "contract creation"),
                        "value_hsk": float(w3.from_wei(tx["value"], "ether")),
                        "block": tx["blockNumber"],
                        "direction": "OUT" if tx["from"].lower() == address.lower() else "IN"
                    })
        except Exception:
            continue
    
    return {
        "address": address,
        "balance_hsk": float(balance_hsk),
        "total_tx_count": tx_count,
        "recent_transactions": recent_txs,
        "network": "testnet" if testnet else "mainnet",
        "block_number": block_number
    }
