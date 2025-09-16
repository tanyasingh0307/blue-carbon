"""
Blockchain service for Web3 interactions and smart contract management
Handles ERC-1155 carbon credit minting, transfers, and marketplace operations
"""

from web3 import Web3
from web3.middleware import geth_poa_middleware
from typing import Optional, Dict, Any
import json
import os
from core.config import settings

class BlockchainService:
    """Service for blockchain interactions and smart contract operations"""
    
    def __init__(self):
        self.w3: Optional[Web3] = None
        self.contract = None
        self.account = None
        self.contract_abi = self._load_contract_abi()
    
    async def initialize(self):
        """Initialize Web3 connection and contract instance"""
        try:
            # Connect to Web3 provider
            self.w3 = Web3(Web3.HTTPProvider(settings.WEB3_PROVIDER_URL))
            
            # Add PoA middleware for testnets
            if "mumbai" in settings.WEB3_PROVIDER_URL.lower():
                self.w3.middleware_onion.inject(geth_poa_middleware, layer=0)
            
            # Check connection
            if not self.w3.is_connected():
                raise Exception("Failed to connect to Web3 provider")
            
            # Set up account from private key
            if settings.PRIVATE_KEY:
                self.account = self.w3.eth.account.from_key(settings.PRIVATE_KEY)
                self.w3.eth.default_account = self.account.address
            
            # Initialize contract if address is provided
            if settings.CONTRACT_ADDRESS and self.contract_abi:
                self.contract = self.w3.eth.contract(
                    address=settings.CONTRACT_ADDRESS,
                    abi=self.contract_abi
                )
            
            print(f"✅ Blockchain service initialized - Network: {self.w3.eth.chain_id}")
            
        except Exception as e:
            print(f"❌ Blockchain initialization failed: {e}")
            raise e
    
    def is_connected(self) -> bool:
        """Check if Web3 is connected"""
        return self.w3 is not None and self.w3.is_connected()
    
    def _load_contract_abi(self) -> Optional[list]:
        """Load contract ABI from file"""
        try:
            abi_path = os.path.join("contracts", "artifacts", "contracts", "BlueCarbonCredits.sol", "BlueCarbonCredits.json")
            if os.path.exists(abi_path):
                with open(abi_path, 'r') as f:
                    contract_json = json.load(f)
                    return contract_json.get('abi', [])
            else:
                # Fallback ABI for ERC-1155
                return self._get_fallback_abi()
        except Exception as e:
            print(f"Warning: Could not load contract ABI: {e}")
            return self._get_fallback_abi()
    
    def _get_fallback_abi(self) -> list:
        """Fallback ERC-1155 ABI for basic operations"""
        return [
            {
                "inputs": [
                    {"name": "to", "type": "address"},
                    {"name": "id", "type": "uint256"},
                    {"name": "amount", "type": "uint256"},
                    {"name": "data", "type": "bytes"}
                ],
                "name": "mint",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function"
            },
            {
                "inputs": [
                    {"name": "account", "type": "address"},
                    {"name": "id", "type": "uint256"}
                ],
                "name": "balanceOf",
                "outputs": [{"name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function"
            },
            {
                "inputs": [
                    {"name": "from", "type": "address"},
                    {"name": "to", "type": "address"},
                    {"name": "id", "type": "uint256"},
                    {"name": "amount", "type": "uint256"},
                    {"name": "data", "type": "bytes"}
                ],
                "name": "safeTransferFrom",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function"
            }
        ]
    
    async def mint_carbon_credits(
        self, 
        to_address: str, 
        token_id: int, 
        amount: int, 
        metadata: Dict[str, Any]
    ) -> Optional[str]:
        """Mint carbon credits as ERC-1155 tokens"""
        try:
            if not self.contract or not self.account:
                raise Exception("Contract or account not initialized")
            
            # Prepare transaction
            function = self.contract.functions.mint(
                to_address,
                token_id,
                amount,
                b""  # Empty data for now
            )
            
            # Build transaction
            transaction = function.build_transaction({
                'from': self.account.address,
                'gas': 200000,
                'gasPrice': self.w3.to_wei('20', 'gwei'),
                'nonce': self.w3.eth.get_transaction_count(self.account.address),
            })
            
            # Sign and send transaction
            signed_txn = self.w3.eth.account.sign_transaction(transaction, settings.PRIVATE_KEY)
            tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
            
            # Wait for transaction receipt
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            
            return receipt.transactionHash.hex()
            
        except Exception as e:
            print(f"Error minting carbon credits: {e}")
            return None
    
    async def transfer_credits(
        self, 
        from_address: str, 
        to_address: str, 
        token_id: int, 
        amount: int
    ) -> Optional[str]:
        """Transfer carbon credits between addresses"""
        try:
            if not self.contract or not self.account:
                raise Exception("Contract or account not initialized")
            
            # Prepare transaction
            function = self.contract.functions.safeTransferFrom(
                from_address,
                to_address,
                token_id,
                amount,
                b""
            )
            
            # Build transaction
            transaction = function.build_transaction({
                'from': self.account.address,
                'gas': 150000,
                'gasPrice': self.w3.to_wei('20', 'gwei'),
                'nonce': self.w3.eth.get_transaction_count(self.account.address),
            })
            
            # Sign and send transaction
            signed_txn = self.w3.eth.account.sign_transaction(transaction, settings.PRIVATE_KEY)
            tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
            
            # Wait for transaction receipt
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            
            return receipt.transactionHash.hex()
            
        except Exception as e:
            print(f"Error transferring credits: {e}")
            return None
    
    async def get_balance(self, address: str, token_id: int) -> int:
        """Get token balance for an address"""
        try:
            if not self.contract:
                return 0
            
            balance = self.contract.functions.balanceOf(address, token_id).call()
            return balance
            
        except Exception as e:
            print(f"Error getting balance: {e}")
            return 0
    
    async def retire_credits(self, token_id: int, amount: int) -> Optional[str]:
        """Retire carbon credits (burn tokens)"""
        try:
            # For now, transfer to a burn address
            burn_address = "0x000000000000000000000000000000000000dEaD"
            return await self.transfer_credits(
                self.account.address,
                burn_address,
                token_id,
                amount
            )
        except Exception as e:
            print(f"Error retiring credits: {e}")
            return None
    
    def get_transaction_receipt(self, tx_hash: str) -> Optional[Dict]:
        """Get transaction receipt by hash"""
        try:
            if not self.w3:
                return None
            
            receipt = self.w3.eth.get_transaction_receipt(tx_hash)
            return {
                'transactionHash': receipt.transactionHash.hex(),
                'blockNumber': receipt.blockNumber,
                'gasUsed': receipt.gasUsed,
                'status': receipt.status
            }
        except Exception as e:
            print(f"Error getting transaction receipt: {e}")
            return None

# Global blockchain service instance
blockchain_service = BlockchainService()