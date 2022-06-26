// SPDX-License-Identifier: MIT
pragma solidity ^0.8.7;

import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@chainlink/contracts/src/v0.8/interfaces/VRFCoordinatorV2Interface.sol";
import "@chainlink/contracts/src/v0.8/VRFConsumerBaseV2.sol";

contract AdvanceCollectible is ERC721URIStorage, VRFConsumerBaseV2 {
    VRFCoordinatorV2Interface Cordinator;
    uint256 tokenCounter;
    bytes32 keyhash;
    uint32 fee;
    uint64 subscriptionId;
    uint32 numwords;
    uint16 requestConfirmations;
    enum Breed {
        PUG,
        SHIBA_INU,
        ST_BERNARD
    }
    mapping(uint256 => Breed) public tokenIdtobreed;
    mapping(uint256 => address) public requestIdtosender;
    event requestCollectible(uint256 indexed requestId, address requester);
    event breedAssigned(uint256 indexed tokenId, Breed breed);

    constructor(
        address _vrfCoordinator,
        bytes32 _keyhash,
        uint32 _fee,
        uint64 _subscriptionId,
        uint32 _numwords,
        uint16 _requestConfirmations
    ) VRFConsumerBaseV2(_vrfCoordinator) ERC721("Doggie", "DOG") {
        tokenCounter = 0;
        keyhash = _keyhash;
        fee = _fee;
        subscriptionId = _subscriptionId;
        requestConfirmations = _requestConfirmations;
        numwords = _numwords;
    }

    uint256 requestId;

    function createCollectible() public returns (uint256) {
        requestId = Cordinator.requestRandomWords(
            keyhash,
            subscriptionId,
            requestConfirmations,
            fee,
            numwords
        );
        requestIdtosender[requestId] = msg.sender;
        emit requestCollectible(requestId, msg.sender);
    }

    function fulfillRandomWords(
        uint256 requestid, /* requestId */
        uint256[] memory randomWords
    ) internal override {
        Breed breed = Breed(randomWords[tokenCounter] % 3);
        uint256 newtokenId = tokenCounter;
        tokenIdtobreed[newtokenId] = breed;
        emit breedAssigned(newtokenId, breed);
        //requestIdtosender[requestId] = msg.sender;
        address owner = requestIdtosender[requestid];
        _safeMint(owner, newtokenId);
        tokenCounter = tokenCounter + 1;
    }

    function setTokenURI(uint256 _newtokenId, string memory _tokenURI) public {
        require(
            _isApprovedOrOwner(_msgSender(), _newtokenId),
            "ERC721: caller is not owner no approval!!...."
        );
        _setTokenURI(_newtokenId, _tokenURI);
    }
}
