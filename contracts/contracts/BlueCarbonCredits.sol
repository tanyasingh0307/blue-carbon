// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "@openzeppelin/contracts/token/ERC1155/ERC1155.sol";
import "@openzeppelin/contracts/access/AccessControl.sol";
import "@openzeppelin/contracts/security/Pausable.sol";
import "@openzeppelin/contracts/token/ERC1155/extensions/ERC1155Burnable.sol";
import "@openzeppelin/contracts/token/ERC1155/extensions/ERC1155Supply.sol";

/**
 * @title BlueCarbonCredits
 * @dev ERC1155 smart contract for Blue Carbon Credits
 * Supports minting, transferring, and retiring (burning) carbon credits
 * with role-based access control for auditors and administrators
 */
contract BlueCarbonCredits is ERC1155, AccessControl, Pausable, ERC1155Burnable, ERC1155Supply {
    
    // Role definitions
    bytes32 public constant AUDITOR_ROLE = keccak256("AUDITOR_ROLE");
    bytes32 public constant PAUSER_ROLE = keccak256("PAUSER_ROLE");
    
    // Contract metadata
    string public name = "Blue Carbon Credits";
    string public symbol = "BCC";
    
    // Token metadata mapping
    mapping(uint256 => TokenMetadata) public tokenMetadata;
    
    // MRV report mapping for transparency
    mapping(uint256 => string) public mrvReports; // tokenId => IPFS hash
    
    // Retirement tracking
    mapping(uint256 => uint256) public retiredSupply;
    mapping(address => mapping(uint256 => uint256)) public retiredBalances;
    
    // Events
    event CreditsMinted(
        uint256 indexed tokenId,
        address indexed to,
        uint256 amount,
        string projectName,
        string projectType,
        uint256 vintage
    );
    
    event CreditsRetired(
        uint256 indexed tokenId,
        address indexed account,
        uint256 amount,
        string reason
    );
    
    event MRVReportUpdated(
        uint256 indexed tokenId,
        string ipfsHash
    );
    
    // Structs
    struct TokenMetadata {
        string projectName;
        string projectType;
        string location;
        uint256 vintage;
        uint256 co2Tons;
        string methodology;
        address auditor;
        uint256 mintTimestamp;
        bool isActive;
    }
    
    /**
     * @dev Constructor sets up the contract with initial admin
     */
    constructor() ERC1155("https://api.bluecarbon.org/metadata/{id}.json") {
        _grantRole(DEFAULT_ADMIN_ROLE, msg.sender);
        _grantRole(AUDITOR_ROLE, msg.sender);
        _grantRole(PAUSER_ROLE, msg.sender);
    }
    
    /**
     * @dev Mint carbon credits (auditor only)
     * @param to Address to mint credits to
     * @param tokenId Unique token ID for the credit batch
     * @param amount Number of credits to mint
     * @param projectName Name of the blue carbon project
     * @param projectType Type of project (mangroves, seagrass, salt_marshes)
     * @param location Project location
     * @param vintage Year the carbon was sequestered
     * @param co2Tons Total CO2 tons represented by this batch
     * @param methodology MRV methodology used
     * @param data Additional data for the mint
     */
    function mintCredits(
        address to,
        uint256 tokenId,
        uint256 amount,
        string memory projectName,
        string memory projectType,
        string memory location,
        uint256 vintage,
        uint256 co2Tons,
        string memory methodology,
        bytes memory data
    ) public onlyRole(AUDITOR_ROLE) whenNotPaused {
        require(to != address(0), "Cannot mint to zero address");
        require(amount > 0, "Amount must be greater than 0");
        require(vintage <= block.timestamp / 365 days + 1970, "Invalid vintage year");
        require(!tokenMetadata[tokenId].isActive, "Token ID already exists");
        
        // Store token metadata
        tokenMetadata[tokenId] = TokenMetadata({
            projectName: projectName,
            projectType: projectType,
            location: location,
            vintage: vintage,
            co2Tons: co2Tons,
            methodology: methodology,
            auditor: msg.sender,
            mintTimestamp: block.timestamp,
            isActive: true
        });
        
        // Mint the tokens
        _mint(to, tokenId, amount, data);
        
        emit CreditsMinted(tokenId, to, amount, projectName, projectType, vintage);
    }
    
    /**
     * @dev Retire carbon credits (burn permanently)
     * @param tokenId Token ID to retire
     * @param amount Number of credits to retire
     * @param reason Reason for retirement
     */
    function retireCredits(
        uint256 tokenId,
        uint256 amount,
        string memory reason
    ) public whenNotPaused {
        require(balanceOf(msg.sender, tokenId) >= amount, "Insufficient balance");
        require(amount > 0, "Amount must be greater than 0");
        
        // Burn the tokens
        _burn(msg.sender, tokenId, amount);
        
        // Update retirement tracking
        retiredSupply[tokenId] += amount;
        retiredBalances[msg.sender][tokenId] += amount;
        
        emit CreditsRetired(tokenId, msg.sender, amount, reason);
    }
    
    /**
     * @dev Set MRV report IPFS hash for transparency
     * @param tokenId Token ID to associate with report
     * @param ipfsHash IPFS hash of the MRV report
     */
    function setMRVReport(
        uint256 tokenId,
        string memory ipfsHash
    ) public onlyRole(AUDITOR_ROLE) {
        require(tokenMetadata[tokenId].isActive, "Token does not exist");
        mrvReports[tokenId] = ipfsHash;
        emit MRVReportUpdated(tokenId, ipfsHash);
    }
    
    /**
     * @dev Get token metadata
     * @param tokenId Token ID to query
     * @return TokenMetadata struct
     */
    function getTokenMetadata(uint256 tokenId) public view returns (TokenMetadata memory) {
        require(tokenMetadata[tokenId].isActive, "Token does not exist");
        return tokenMetadata[tokenId];
    }
    
    /**
     * @dev Get retirement information for an account and token
     * @param account Account to query
     * @param tokenId Token ID to query
     * @return Number of retired credits
     */
    function getRetiredBalance(address account, uint256 tokenId) public view returns (uint256) {
        return retiredBalances[account][tokenId];
    }
    
    /**
     * @dev Get total retired supply for a token
     * @param tokenId Token ID to query
     * @return Total retired supply
     */
    function getTotalRetired(uint256 tokenId) public view returns (uint256) {
        return retiredSupply[tokenId];
    }
    
    /**
     * @dev Pause contract (emergency use)
     */
    function pause() public onlyRole(PAUSER_ROLE) {
        _pause();
    }
    
    /**
     * @dev Unpause contract
     */
    function unpause() public onlyRole(PAUSER_ROLE) {
        _unpause();
    }
    
    /**
     * @dev Set new URI for metadata
     * @param newuri New URI string
     */
    function setURI(string memory newuri) public onlyRole(DEFAULT_ADMIN_ROLE) {
        _setURI(newuri);
    }
    
    /**
     * @dev Grant auditor role to address
     * @param account Address to grant role to
     */
    function grantAuditorRole(address account) public onlyRole(DEFAULT_ADMIN_ROLE) {
        _grantRole(AUDITOR_ROLE, account);
    }
    
    /**
     * @dev Revoke auditor role from address
     * @param account Address to revoke role from
     */
    function revokeAuditorRole(address account) public onlyRole(DEFAULT_ADMIN_ROLE) {
        _revokeRole(AUDITOR_ROLE, account);
    }
    
    // Override functions for multiple inheritance
    function _beforeTokenTransfer(
        address operator,
        address from,
        address to,
        uint256[] memory ids,
        uint256[] memory amounts,
        bytes memory data
    ) internal override(ERC1155, ERC1155Supply) whenNotPaused {
        super._beforeTokenTransfer(operator, from, to, ids, amounts, data);
    }
    
    function supportsInterface(bytes4 interfaceId)
        public
        view
        override(ERC1155, AccessControl)
        returns (bool)
    {
        return super.supportsInterface(interfaceId);
    }
}