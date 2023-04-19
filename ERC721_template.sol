pragma solidity ^0.8.0;

import "node_modules/@openzeppelin/contracts/token/ERC721/ERC721.sol";

contract GB_NFT is ERC721 {
    string private _name;
    string private _symbol;

    constructor(string memory name, string memory symbol) ERC721(name, symbol) {
        _name = name;
        _symbol = symbol;
    }

    function mint(address to, uint256 tokenId) public {
        _mint(to, tokenId);
    }

    function updateNameAndSymbol(string memory name, string memory symbol) public {
        require(_isApprovedOrOwner(msg.sender, 1), "Only the owner can update the name and symbol");
        _name = name;
        _symbol = symbol;
    }

    function name() public view virtual override returns (string memory) {
        return _name;
    }

    function symbol() public view virtual override returns (string memory) {
        return _symbol;
    }
}