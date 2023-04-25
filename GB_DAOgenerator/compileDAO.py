from web3 import Web3
import solcx
from solcx import compile_source
import json
import os
def main(name, symbol, address, votingPeriod):
    # Version de compilador para el bloque ERC721_template
    solcx.install_solc('0.8.9')
    solcx.set_solc_version('0.8.9')
    # Connexión a blockchain RPC ie Ganache
    web3 = Web3(Web3.HTTPProvider('http://127.0.0.1:9545'))

    contract_source_code = '''
    pragma solidity ^0.8.9;

    import "node_modules/@openzeppelin/contracts/token/ERC20/ERC20.sol";
    import "node_modules/@openzeppelin/contracts/token/ERC20/extensions/ERC20Burnable.sol";
    import "node_modules/@openzeppelin/contracts/access/Ownable.sol";
    import "node_modules/@openzeppelin/contracts/token/ERC20/extensions/draft-ERC20Permit.sol";
    import "node_modules/@openzeppelin/contracts/token/ERC20/extensions/ERC20Votes.sol";

    contract GB_ERC20 is ERC20, ERC20Burnable, Ownable, ERC20Permit, ERC20Votes {

    event VoteCast(address indexed voter, uint256 proposalId, bool support, string reason);

    constructor(string memory name, string memory symbol ) ERC20(name, symbol) ERC20Permit(name) {}

    function mint(address to, uint256 amount) public onlyOwner {
        _mint(to, amount);
    }

    // The following functions are overrides required by Solidity.

    function _castVote(address voter, uint256 proposalId, bool support, string memory reason) public {
        emit VoteCast(voter, proposalId, support, reason);
        _castVote(voter, proposalId, support, reason);
    }
    function _afterTokenTransfer(address from, address to, uint256 amount)
        internal
        override(ERC20, ERC20Votes)
    {
        super._afterTokenTransfer(from, to, amount);
    }

    function _mint(address to, uint256 amount)
        internal
        override(ERC20, ERC20Votes)
    {
        super._mint(to, amount);
    }

    function _burn(address account, uint256 amount)
        internal
        override(ERC20, ERC20Votes)
    {
        super._burn(account, amount);
    }
}
    
    '''
    # template_path = os.path.join(os.path.dirname(__file__), 'ERC20voting_template.sol')
    # with open(template_path, 'r') as f:
    #     contract_source_code = f.read()

    dao_contract_source_code = '''
    // SPDX-License-Identifier: MIT
    pragma solidity ^0.8.9;

    import "./ERC20voting_template.sol";

    contract GB_DAO {
        GB_ERC20 public governanceToken;
        address public daoGovernor;
        uint public votingPeriod;

        struct Proposal {
            string title;
            string description;
            uint forVotes;
            uint againstVotes;
            bool executed;
            bool passed;
            address PropCreator;
            uint votingDeadline;
        }

        Proposal[] public proposals;
        uint public proposalCount;

        constructor(address _governanceToken, uint _votingPeriod) {
            governanceToken = GB_ERC20(_governanceToken);
            daoGovernor = msg.sender;
            proposalCount = 0;
            votingPeriod = _votingPeriod;
        }

        modifier onlyGovernor() {
            require(msg.sender == daoGovernor, "Only the DAO governor can perform this action");
            _;
        }

        function updateGovernor(address newGovernor) public onlyGovernor {
            daoGovernor = newGovernor;
        }

        function mintTokens(address recipient, uint256 amount) public onlyGovernor {
            governanceToken.mint(recipient, amount);
        }

        function burnTokens(address account, uint256 amount) public onlyGovernor {
            governanceToken.burn(amount);
        }

        function transferTokens(address recipient, uint256 amount) public onlyGovernor {
            governanceToken.transfer(recipient, amount);
        }

        function vote(address voter, uint proposalId, string memory reason) public {
            Proposal storage proposal = proposals[proposalId];
            require(block.timestamp <= proposal.votingDeadline, "Voting has ended for this proposal");
            governanceToken._castVote(voter, proposalId, true , reason );
        }

        function revokeVote(address voter, uint proposalId) public {
            Proposal storage proposal = proposals[proposalId];
            require(block.timestamp <= proposal.votingDeadline, "Voting has ended for this proposal");

            governanceToken._castVote(voter, proposalId, false, "revoked");
        }

        function createProposal(string memory title, string memory description) public onlyGovernor {
            proposals.push(Proposal(title, description, 0, 0, false, false, daoGovernor,block.timestamp + votingPeriod));
            proposalCount += 1;
        }

        function getProposal(uint proposalId) public view returns (string memory title, string memory description, uint forVotes, uint againstVotes, bool executed, bool passed, uint votingDeadline) {
            Proposal storage proposal = proposals[proposalId];
            return (proposal.title, proposal.description, proposal.forVotes, proposal.againstVotes, proposal.executed, proposal.passed, proposal.votingDeadline);
        }
    }
    '''

    # Compilación de contrato
    compiled_sol = compile_source(dao_contract_source_code)
    contract_interface = compiled_sol['<stdin>:GB_DAO']

    ERC20_compiled_sol = compile_source(contract_source_code)
    ERC20_contract_interface = ERC20_compiled_sol['<stdin>:GB_ERC20']

    # Despliegue de contrato erc20
    ERC20_contract = web3.eth.contract(abi=ERC20_contract_interface['abi'], bytecode=ERC20_contract_interface['bin'])
    tx_hash = ERC20_contract.constructor(name,symbol).transact({'from': str(address)})
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    erc20_contract_address = tx_receipt.contractAddress
    #Importante: identifica la wallet que va a ser creadora del contrato

    # Despliegue de contrato

    contract = web3.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])
    tx_hash = contract.constructor(str(erc20_contract_address),int(votingPeriod)).transact({'from': str(address)})
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

    contract_address = tx_receipt.contractAddress
    contract_instance = web3.eth.contract(address=contract_address, abi=contract_interface['abi'])


    print(f"Contract deployed at address: {contract_address}")


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