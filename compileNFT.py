from web3 import Web3
import solcx
from solcx import compile_source
import json
import os


solcx.install_solc('0.8.1')

## Wallet to deploy 0x5174BB860B9427158eDD6B03121A6cBe1baA1438



# Connect to the local blockchain network (Ganache)
web3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))

template_path = os.path.join(os.path.dirname(__file__), 'ERC721_template.sol')
with open(template_path, 'r') as f:
    contract_source_code = f.read()

# Compile the contract source code
"""
contract_source_code = '''
pragma solidity ^0.8.0;
import "node_modules/@openzeppelin/contracts/token/ERC721/ERC721.sol";
contract GB_NFT is ERC721 {
    constructor(string memory name, string memory symbol) ERC721(name, symbol) {
    }
}
'''
"""
compiled_sol = compile_source(contract_source_code)
contract_interface = compiled_sol['<stdin>:GB_NFT']

# Deploy the contract
contract = web3.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])
tx_hash = contract.constructor('MyNFT', 'MNFT').transact({'from': '0x5174BB860B9427158eDD6B03121A6cBe1baA1438'})
tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
contract_address = tx_receipt.contractAddress

contract_instance = web3.eth.contract(address=contract_address, abi=contract_interface['abi'])
# PARA HACER - Implementar interacciones con contrato -> no está funcionando 

# # Interact with the contract to change the name and symbol values
# tx_hash = contract_instance.functions.updateNameAndSymbol('MyNewNFT', 'MNNFT').transact()
# # web3.eth.waitForTransactionReceipt(tx_hash)
# web3.eth.wait_for_transaction_receipt(tx_hash)

# Get the updated name and symbol values
name = contract_instance.functions.name().call()
symbol = contract_instance.functions.symbol().call()

print(f"Contract deployed at address: {contract_address}")
print(f"Updated name: {name}")
print(f"Updated symbol: {symbol}")
