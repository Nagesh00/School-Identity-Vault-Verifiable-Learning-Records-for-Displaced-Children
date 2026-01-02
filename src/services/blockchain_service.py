"""
Blockchain integration service for tamper-proof record storage
"""
import hashlib
import uuid
from datetime import datetime
from typing import Optional, Dict
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend

try:
    from web3 import Web3
    WEB3_AVAILABLE = True
except ImportError:
    WEB3_AVAILABLE = False

from ..models.schemas import BlockchainRecord, LearningProfile


class BlockchainService:
    """Service for blockchain integration and cryptographic operations"""
    
    def __init__(self, rpc_url: Optional[str] = None, private_key: Optional[str] = None):
        self.w3 = None
        self.account = None
        
        if rpc_url and private_key and WEB3_AVAILABLE:
            try:
                self.w3 = Web3(Web3.HTTPProvider(rpc_url))
                self.account = self.w3.eth.account.from_key(private_key)
            except Exception:
                # Fallback to simulation mode
                pass
        
        # Generate RSA key pair for signing
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        self.public_key = self.private_key.public_key()
    
    def hash_profile(self, profile: LearningProfile) -> str:
        """Create cryptographic hash of learning profile"""
        # Create a deterministic string representation
        profile_str = (
            f"{profile.profile_id}|"
            f"{profile.student_name}|"
            f"{profile.student_id or ''}|"
            f"{','.join(profile.documents)}|"
            f"{len(profile.subjects_completed)}|"
            f"{profile.overall_confidence}"
        )
        
        # Calculate SHA-256 hash
        return hashlib.sha256(profile_str.encode()).hexdigest()
    
    def sign_hash(self, data_hash: str) -> str:
        """Create digital signature for data hash"""
        signature = self.private_key.sign(
            data_hash.encode(),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return signature.hex()
    
    def verify_signature(self, data_hash: str, signature_hex: str) -> bool:
        """Verify digital signature"""
        try:
            signature = bytes.fromhex(signature_hex)
            self.public_key.verify(
                signature,
                data_hash.encode(),
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            return True
        except Exception:
            return False
    
    async def store_on_blockchain(
        self,
        profile: LearningProfile
    ) -> BlockchainRecord:
        """Store profile hash and signature on blockchain"""
        record_id = str(uuid.uuid4())
        
        # Create hash
        profile_hash = self.hash_profile(profile)
        
        # Create signature
        signature = self.sign_hash(profile_hash)
        
        # Store on blockchain (if available)
        transaction_hash = None
        block_number = None
        
        if self.w3 and self.w3.is_connected() and self.account:
            try:
                # Simple transaction to store hash (in real implementation, 
                # this would call a smart contract)
                tx = {
                    'from': self.account.address,
                    'to': self.account.address,  # Self-transaction for demo
                    'value': 0,
                    'gas': 21000,
                    'gasPrice': self.w3.eth.gas_price,
                    'nonce': self.w3.eth.get_transaction_count(self.account.address),
                    'data': profile_hash.encode().hex()
                }
                
                signed_tx = self.account.sign_transaction(tx)
                tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
                transaction_hash = tx_hash.hex()
                
                # Wait for transaction receipt
                receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
                block_number = receipt['blockNumber']
            except Exception as e:
                # Blockchain operation failed, continue with local record
                print(f"Blockchain storage failed: {e}")
        
        # Create blockchain record
        record = BlockchainRecord(
            record_id=record_id,
            profile_id=profile.profile_id,
            document_hash=profile_hash,
            signature=signature,
            transaction_hash=transaction_hash,
            block_number=block_number
        )
        
        return record
    
    def verify_blockchain_record(
        self,
        record: BlockchainRecord,
        profile: LearningProfile
    ) -> bool:
        """Verify blockchain record against profile"""
        # Recalculate hash
        current_hash = self.hash_profile(profile)
        
        # Check hash matches
        if current_hash != record.document_hash:
            return False
        
        # Verify signature
        return self.verify_signature(record.document_hash, record.signature)
    
    def get_public_key_pem(self) -> str:
        """Get public key in PEM format"""
        pem = self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        return pem.decode('utf-8')
