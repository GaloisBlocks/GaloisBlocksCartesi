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