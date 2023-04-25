from web3 import Web3
import json
import random

web3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))

with open('contractInfo.json', 'r') as f:
    contract_info = json.load(f)

ABI = contract_info['abi']
contract_address = contract_info['contract_address']

# Cuenta para deploy
deploy_address = web3.eth.accounts[0]

#Esta variable es la que interactua con el servicio frontend
interaction_address = deploy_address
contract_instance = web3.eth.contract(address=contract_address,abi=ABI)

# Ejemplo: Mintear un NFT del contrato con un ID dado a

def mintTokens(toAddress, fromAddress, amount, contract_instance):
    # Mint amount token
    try:
        tx_mint = contract_instance.functions.mint(toAddress, amount).transact({'from': fromAddress})
        tx_receipt = web3.eth.wait_for_transaction_receipt(tx_mint)
    except Exception as e:
        return "Error minting ERC20"

    return f"{amount} ERC20 tokens minteados a {toAddress}"
 
def burnTokens(fromAddress, amount, contract_instance):
    # Mint amount token
    try:
        tx_mint = contract_instance.functions.burn(amount).transact({'from': fromAddress})
        tx_receipt = web3.eth.wait_for_transaction_receipt(tx_mint)
    except Exception as e:
        return "Error burning ERC20"

    return f"{amount} ERC20 tokens quemados :fuego:"

amount = 10
x = mintTokens(interaction_address,interaction_address,amount,contract_instance)
print(x)
y = burnTokens(interaction_address,amount,contract_instance)
print("  ")
print(y)