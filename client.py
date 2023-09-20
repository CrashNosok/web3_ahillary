from web3 import Web3
from eth_account.signers.local import LocalAccount


class Client:
    def __init__(self, private_key: str, rpc: str):
        self.w3 = Web3(Web3.HTTPProvider(endpoint_uri=rpc))
        self.account: LocalAccount = self.w3.eth.account.from_key(private_key=private_key)

    def send_transaction(self, to, data=None, value=None):
        tx_params = {
            'chainId': self.w3.eth.chain_id,
            'nonce': self.w3.eth.get_transaction_count(self.account.address),
            'from': self.account.address,
            'to': Web3.to_checksum_address(to),
            'gasPrice': self.w3.eth.gas_price
        }
        if data:
            tx_params['data'] = data
        if value:
            tx_params['value'] = value

        try:
            tx_params['gas'] = self.w3.eth.estimate_gas(tx_params)
        except Exception as err:
            print(f'{self.account.address} | Transaction failed | {err}')
            return None

        sign = self.w3.eth.account.sign_transaction(tx_params, self.account.key)
        tx_hash = self.w3.eth.send_raw_transaction(sign.rawTransaction)
        data = self.w3.eth.wait_for_transaction_receipt(transaction_hash=tx_hash, timeout=200)

        if 'status' in data and data['status'] == 1:
            print(f'{self.account.address} | transaction was successful: {tx_hash.hex()}')
            return True
        print(f'{self.account.address} | transaction failed {data["transactionHash"].hex()}')
        return False
