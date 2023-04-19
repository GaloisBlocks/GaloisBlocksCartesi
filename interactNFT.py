from web3 import Web3
import json

web3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))

with open('contractInfo_8.json', 'r') as f:
    contract_info = json.load(f)

ABI = contract_info['abi']
contract_address = contract_info['contract_address']
interaction_address = web3.eth.accounts[0]
contract_instance = web3.eth.contract(address=contract_address,abi=ABI)

# Ejemplo: Mintear un NFT del contrato con un ID dado a
def mintNFT(toAddress, fromAddress, tokenID, contract_instance):
    # Mint hacia self_address con TokenID dado
    try:
        tx_mint = contract_instance.functions.mint(toAddress, tokenID).transact({'from': fromAddress})
    except Exception as e:
        return "tokenID no disponible, ya minteado"

def changeNameSymbol(ownerAddress, newName, newSymbol, contract_instance):
    try:
        tx_hash = contract_instance.functions.updateNameAndSymbol(newName, newSymbol).transact({'from':ownerAddress})
    except Exception as e:
        return "cartera seleccionada no es dueña del contrato"
    

# Ejemplo: Minteamos y cambiamos nombre

name, symbol = contract_instance.functions.name().call() , contract_instance.functions.symbol().call()
print(name,symbol)

mintNFT(interaction_address,interaction_address,3,contract_instance)
changeNameSymbol("0x85C5AbD48fe34258af20451f90934e7E0c39D9C8","lamamalona xdd","LMMxD",contract_instance)

name, symbol = contract_instance.functions.name().call() , contract_instance.functions.symbol().call()
print(name,symbol)
