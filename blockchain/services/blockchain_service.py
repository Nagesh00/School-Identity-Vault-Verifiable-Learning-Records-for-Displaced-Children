"""
Blockchain Integration Module
Web3 integration for recording verifications on blockchain
"""
import os
import logging
from typing import Dict, Any
from web3 import Web3
from dotenv import load_dotenv
import json

load_dotenv()
logger = logging.getLogger(__name__)


class BlockchainService:
    """Service for recording verifications on blockchain"""
    
    def __init__(self):
        # Initialize Web3 connection
        blockchain_url = os.getenv("BLOCKCHAIN_RPC_URL")
        self.w3 = Web3(Web3.HTTPProvider(blockchain_url))
        
        # Load contract ABI
        with open("blockchain/contracts/abi/VerificationRecord.json") as f:
            self.contract_abi = json.load(f)
        
        # Initialize contract
        contract_address = os.getenv("CONTRACT_ADDRESS")
        self.contract = self.w3.eth.contract(
            address=Web3.toChecksumAddress(contract_address),
            abi=self.contract_abi
        )
        
        self.account = self.w3.eth.account.from_key(os.getenv("PRIVATE_KEY"))
    
    def record_document(self, document_hash: str, document_type: str, 
                       metadata: Dict[str, Any]) -> Dict[str, Any]:
        """
        Record document on blockchain
        
        Args:
            document_hash: Hash of document
            document_type: Type of document (certificate, report_card, etc.)
            metadata: Document metadata
        
        Returns:
            Transaction receipt
        """
        try:
            logger.info(f"Recording document on blockchain: {document_hash}")
            
            # Prepare transaction
            tx = self.contract.functions.recordDocument(
                bytes.fromhex(document_hash.lstrip('0x')),
                document_type,
                json.dumps(metadata).encode()
            ).buildTransaction({
                'from': self.account.address,
                'nonce': self.w3.eth.get_transaction_count(self.account.address),
                'gas': 200000,
                'gasPrice': self.w3.eth.gas_price,
            })
            
            # Sign transaction
            signed_tx = self.w3.eth.account.sign_transaction(tx, self.account.key)
            
            # Send transaction
            tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            
            logger.info(f"Document recorded: {receipt['transactionHash'].hex()}")
            
            return {
                "success": True,
                "transactionHash": receipt['transactionHash'].hex(),
                "blockNumber": receipt['blockNumber'],
                "status": receipt['status']
            }
            
        except Exception as e:
            logger.error(f"Error recording document: {str(e)}")
            raise
    
    def record_verification(self, profile_hash: str, verification_hash: str,
                           is_verified: bool, notes: str) -> Dict[str, Any]:
        """
        Record verification on blockchain
        """
        try:
            logger.info(f"Recording verification on blockchain: {verification_hash}")
            
            tx = self.contract.functions.recordVerification(
                bytes.fromhex(verification_hash.lstrip('0x')),
                bytes.fromhex(profile_hash.lstrip('0x')),
                is_verified,
                notes
            ).buildTransaction({
                'from': self.account.address,
                'nonce': self.w3.eth.get_transaction_count(self.account.address),
                'gas': 200000,
                'gasPrice': self.w3.eth.gas_price,
            })
            
            signed_tx = self.w3.eth.account.sign_transaction(tx, self.account.key)
            tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            
            logger.info(f"Verification recorded: {receipt['transactionHash'].hex()}")
            
            return {
                "success": True,
                "transactionHash": receipt['transactionHash'].hex(),
                "blockNumber": receipt['blockNumber'],
                "status": receipt['status']
            }
            
        except Exception as e:
            logger.error(f"Error recording verification: {str(e)}")
            raise
    
    def get_verification_history(self, profile_hash: str):
        """Retrieve verification history for a profile"""
        try:
            history = self.contract.functions.getVerificationHistory(
                bytes.fromhex(profile_hash.lstrip('0x'))
            ).call()
            
            return {
                "success": True,
                "verificationHashes": [h.hex() for h in history]
            }
            
        except Exception as e:
            logger.error(f"Error retrieving verification history: {str(e)}")
            raise
