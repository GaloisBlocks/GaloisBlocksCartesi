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

def mintNFT(toAddress, fromAddress, metadata, contract_instance):
    # Obtenemos max supply para saber los tokens no utilizados
    max_supply = contract_instance.functions.maxSupply().call()
    # Evaluamos tokens no utilizados
    while True:
        token_id = random.randint(1,max_supply)
        if not contract_instance.functions.exists(token_id).call():
            break

    # Mint NFT con token random generado
    try:
        tx_mint = contract_instance.functions.mint(toAddress, metadata).transact({'from': fromAddress})
        
        tx_receipt = web3.eth.wait_for_transaction_receipt(tx_mint)
    except Exception as e:
        return "Error minting NFT"

    return f"NFT minteado a {toAddress} con token ID {token_id}"

def changeNameSymbol(ownerAddress, newName, newSymbol, contract_instance):
    try:
        prev_name, prev_symbol = contract_instance.functions.name().call() , contract_instance.functions.symbol().call()
        tx_hash = contract_instance.functions.updateNameAndSymbol(newName, newSymbol).transact({'from':ownerAddress})

        newName, newSymbol = contract_instance.functions.name().call() , contract_instance.functions.symbol().call()
        return f"Contrato NFT cambió su nombre y símbolo de ({prev_name},{prev_symbol}) ----> ({newName},{newSymbol}) "
    except Exception as e:
        return "Error cambiando el nombre o símbolo, verifica si todo está en orden"
    

# Ejemplo: Minteamos y cambiamos nombre

# Desde Frontend obtenemos nuevos valores:
newTokenMetadata = "ipfs://bafyreib6mpqau2amz2ilmcxpbkyabolr5xt4szxxy75rkgyffoc6dnjcta/metadata.json"
x = mintNFT(interaction_address,interaction_address,newTokenMetadata,contract_instance)

name, symbol = contract_instance.functions.name().call() , contract_instance.functions.symbol().call()

newName = "NFT testingOMGworks"
newSymbol = "NFTworks"
y = changeNameSymbol(deploy_address,newName,newSymbol,contract_instance)
name, symbol = contract_instance.functions.name().call() , contract_instance.functions.symbol().call()

print(x)
print("  ")
print(y)