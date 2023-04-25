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