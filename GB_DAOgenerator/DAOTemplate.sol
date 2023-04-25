// SPDX-License-Identifier: MIT
pragma solidity ^0.8.9;

import "./ERC20voting_template.sol";

contract DAO {
    GB_ERC20 public governanceToken;
    address public daoGovernor;

    struct Proposal {
        string title;
        string description;
        uint forVotes;
        uint againstVotes;
        bool executed;
        bool passed;
    }

    Proposal[] public proposals;
    uint public proposalCount;

    constructor(address _governanceToken) {
        governanceToken = GB_ERC20(_governanceToken);
        daoGovernor = msg.sender;
        proposalCount = 0;
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
        governanceToken.burn(account, amount);
    }

    function transferTokens(address recipient, uint256 amount) public onlyGovernor {
        governanceToken.transfer(recipient, amount);
    }

    function vote(uint proposalId) public {
        governanceToken.castVote(proposalId, true);
    }

    function revokeVote(uint proposalId) public {
        governanceToken.castVote(proposalId, false);
    }
    function createProposal(string memory title, string memory description) public onlyGovernor {
        proposals.push(Proposal(title, description, 0, 0, false, false));
        proposalCount += 1;
    }

    function getProposal(uint proposalId) public view returns (string memory title, string memory description, uint forVotes, uint againstVotes, bool executed, bool passed) {
        Proposal storage proposal = proposals[proposalId];
        return (proposal.title, proposal.description, proposal.forVotes, proposal.againstVotes, proposal.executed, proposal.passed);
    }

}
