from web3 import Web3
import os

HASHKEY_RPC = os.getenv("HASHKEY_RPC_URL", "https://mainnet.hsk.xyz")
HASHKEY_TESTNET_RPC = os.getenv("HASHKEY_TESTNET_RPC_URL", "https://mainnet.hsk.xyz")

def get_web3(testnet: bool = False) -> Web3:
    rpc = HASHKEY_TESTNET_RPC if testnet else HASHKEY_RPC
    return Web3(Web3.HTTPProvider(rpc, request_kwargs={"timeout": 10}))

def get_wallet_data(address: str, testnet: bool = False) -> dict:
    """Fetch wallet balance, tx count, and recent transactions."""
    w3 = get_web3(testnet)

    if not w3.is_connected():
        raise ConnectionError("Could not connect to HashKey Chain RPC")

    checksum_address = w3.to_checksum_address(address)
    balance_wei = w3.eth.get_balance(checksum_address)
    balance_hsk = float(w3.from_wei(balance_wei, "ether"))
    tx_count = w3.eth.get_transaction_count(checksum_address)
    block_number = w3.eth.block_number

    # Scan recent blocks for transactions (limit to 20 blocks for speed)
    recent_txs = []
    scan_limit = 20
    for i in range(block_number, max(0, block_number - scan_limit), -1):
        if len(recent_txs) >= 10:
            break
        try:
            block = w3.eth.get_block(i, full_transactions=True)
            for tx in block.transactions:
                tx_from = (tx.get("from") or "").lower()
                tx_to = (tx.get("to") or "").lower()
                addr_lower = address.lower()
                if tx_from == addr_lower or tx_to == addr_lower:
                    recent_txs.append({
                        "hash": tx["hash"].hex(),
                        "from": tx["from"],
                        "to": tx.get("to") or "contract creation",
                        "value_hsk": float(w3.from_wei(tx["value"], "ether")),
                        "block": tx["blockNumber"],
                        "direction": "OUT" if tx_from == addr_lower else "IN"
                    })
        except Exception:
            continue

    return {
        "address": address,
        "balance_hsk": balance_hsk,
        "total_tx_count": tx_count,
        "recent_transactions": recent_txs,
        "network": "testnet" if testnet else "mainnet",
        "block_number": block_number
    }
