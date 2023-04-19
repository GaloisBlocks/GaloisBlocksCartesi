from web3 import Web3
import solcx
from solcx import compile_source
import json
import os
import ipfshttpclient

# Version de compilador para el bloque ERC721_template
solcx.install_solc('0.8.1')

# Connexión a blockchain RPC ie Ganache
web3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))

template_path = os.path.join(os.path.dirname(__file__), 'ERC721_template.sol')
with open(template_path, 'r') as f:
    contract_source_code = f.read()

# Compilación de contrato
compiled_sol = compile_source(contract_source_code)
contract_interface = compiled_sol['<stdin>:GB_NFT']

#Importante: identifica la wallet que va a ser creadora del contrato
deploy_address = web3.eth.accounts[0]

# Despliegue de contrato
contract = web3.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])
tx_hash = contract.constructor('MyNFT', 'MNFT').transact({'from': deploy_address})
tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
contract_address = tx_receipt.contractAddress

contract_instance = web3.eth.contract(address=contract_address, abi=contract_interface['abi'])

name = contract_instance.functions.name().call()
symbol = contract_instance.functions.symbol().call()

print(f"Contract deployed at address: {contract_address}")
print(f"Name: {name}")
print(f"Symbol: {symbol}")


# Define the data to be stored in the JSON file
data = {
    "abi": contract_interface["abi"],
    "contract_address": contract_address
}

# Local Workaround: Se guarda localmente el último ABI y contrato generado

block_number = int(web3.eth.get_block('latest')['number'])

with open("contractInfo.json", "w") as f:
    json.dump(data, f)
print(deploy_address)
# A este punto el contrato YA está generado
# Las interacciones se ejecutarán desde otro py, a saber interactNFT

#TO-DO Post Hackathon: Implementar servicio de subir/bajar ABI y contract Address hacia/de IPFS 