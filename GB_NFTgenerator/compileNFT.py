from web3 import Web3
import solcx
from solcx import compile_source
import json
import os
import ipfshttpclient
def main(name, symbol, address, maxSupply):
    # Version de compilador para el bloque ERC721_template
    solcx.install_solc('0.8.1')

    # Connexión a blockchain RPC ie Ganache
    web3 = Web3(Web3.HTTPProvider('http://127.0.0.1:9545'))

    # template_path = os.path.join(os.path.dirname(__file__), 'ERC721_template.sol')
    # with open(template_path, 'r') as f:
    #     contract_source_code = f.read()
    contract_source_code = '''
    pragma solidity ^0.8.0;

    import "node_modules/@openzeppelin/contracts/token/ERC721/ERC721.sol";
    import "node_modules/@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
    import "node_modules/@openzeppelin/contracts/token/ERC721/extensions/ERC721Enumerable.sol";
    import "node_modules/@openzeppelin/contracts/utils/Counters.sol";
    import "node_modules/@openzeppelin/contracts/access/Ownable.sol";


    contract GB_NFT is ERC721URIStorage, Ownable {
    using Counters for Counters.Counter;
    Counters.Counter private _tokenIds;

    string public _name;
    string public _symbol;
    uint256 public _totalSupply;
    uint256 public _maxSupply;

    constructor(string memory name, string memory symbol, uint256 maxSupply) ERC721(name, symbol) {
        _name = name;
        _symbol = symbol;
        _maxSupply = maxSupply;
    }

    function mint(address to, string memory tokenURI)
        public onlyOwner 
        returns (uint256)
    {
        require(_totalSupply < _maxSupply, "max Supply reached");
        _tokenIds.increment();

        uint256 newItemId = _tokenIds.current();
        _mint(to, newItemId);
        _setTokenURI(newItemId, tokenURI);

        _totalSupply++;

        return newItemId;
    }

    function updateNameAndSymbol(string memory name, string memory symbol) public onlyOwner {
        _name = name;
        _symbol = symbol;
    }


    function name() public view virtual override returns (string memory) {
        return _name;
    }

    function symbol() public view virtual override returns (string memory) {
        return _symbol;
    }

    function totalSupply() public view returns (uint256) {
        return _totalSupply;
    }
    function maxSupply() public view returns (uint256) {
        return _maxSupply;
    }

    function exists(uint256 tokenId) public view returns (bool) {
        return _exists(tokenId);
        }
    }
    '''
    # Compilación de contrato
    compiled_sol = compile_source(contract_source_code)
    contract_interface = compiled_sol['<stdin>:GB_NFT']

    # Importante: identifica la wallet que va a ser creadora del contrato
    # deploy_address = web3.eth.accounts[0]
    # Importante: parámetro del usuario para su NFT, maximo numero de NFTs
    # maxSupply = 51

    # Despliegue de contrato
    contract = web3.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])
    tx_hash = contract.constructor(name,symbol,maxSupply).transact({'from': address})
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
        "contract_address": contract_address,
        "contract_name": name,
        "contract_sym": symbol
    }

    # Local Workaround: Se guarda localmente el último ABI y contrato generado

    block_number = int(web3.eth.get_block('latest')['number'])

    with open("contractInfo.json", "w") as f:
        json.dump(data, f)
    return data
# A este punto el contrato YA está generado
# Las interacciones se ejecutarán desde otro py, a saber interactNFT

#TO-DO Post Hackathon: Implementar servicio de subir/bajar ABI y contract Address hacia/de IPFS 