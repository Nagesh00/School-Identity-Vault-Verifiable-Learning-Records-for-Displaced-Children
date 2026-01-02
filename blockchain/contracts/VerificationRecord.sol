// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/**
 * @title VerificationRecord
 * @dev Smart contract for recording and verifying educational documents on blockchain
 * 
 * Stores:
 * - Document hashes
 * - Verification signatures
 * - Audit trail of all validations
 */

contract VerificationRecord {
    
    // Data structures
    struct Document {
        bytes32 documentHash;
        uint256 timestamp;
        address uploader;
        string documentType;
        bytes metadata;
    }
    
    struct Verification {
        bytes32 verificationHash;
        address verifier;
        bool isVerified;
        uint256 timestamp;
        string notes;
        bytes signature;
    }
    
    struct Profile {
        bytes32 profileHash;
        address child;
        bytes32[] documentHashes;
        bytes32[] verificationHashes;
        uint256 createdAt;
        uint256 lastModified;
    }
    
    // State variables
    mapping(bytes32 => Document) public documents;
    mapping(bytes32 => Verification) public verifications;
    mapping(bytes32 => Profile) public profiles;
    mapping(address => bytes32[]) public userProfiles;
    
    // Events
    event DocumentRecorded(
        bytes32 indexed documentHash,
        address indexed uploader,
        string documentType,
        uint256 timestamp
    );
    
    event ProfileCreated(
        bytes32 indexed profileHash,
        address indexed child,
        uint256 timestamp
    );
    
    event VerificationRecorded(
        bytes32 indexed verificationHash,
        bytes32 indexed profileHash,
        address indexed verifier,
        bool isVerified,
        uint256 timestamp
    );
    
    event VerificationSigned(
        bytes32 indexed verificationHash,
        address indexed verifier,
        uint256 timestamp
    );
    
    // Functions
    
    /**
     * @dev Record a document hash on blockchain
     */
    function recordDocument(
        bytes32 documentHash,
        string memory documentType,
        bytes memory metadata
    ) public {
        require(documentHash != bytes32(0), "Invalid document hash");
        
        Document storage doc = documents[documentHash];
        doc.documentHash = documentHash;
        doc.timestamp = block.timestamp;
        doc.uploader = msg.sender;
        doc.documentType = documentType;
        doc.metadata = metadata;
        
        emit DocumentRecorded(documentHash, msg.sender, documentType, block.timestamp);
    }
    
    /**
     * @dev Create a new learning profile
     */
    function createProfile(
        bytes32 profileHash,
        address childAddress,
        bytes32[] memory documentHashes
    ) public {
        require(profileHash != bytes32(0), "Invalid profile hash");
        require(childAddress != address(0), "Invalid child address");
        
        Profile storage profile = profiles[profileHash];
        profile.profileHash = profileHash;
        profile.child = childAddress;
        profile.documentHashes = documentHashes;
        profile.createdAt = block.timestamp;
        profile.lastModified = block.timestamp;
        
        userProfiles[childAddress].push(profileHash);
        
        emit ProfileCreated(profileHash, childAddress, block.timestamp);
    }
    
    /**
     * @dev Record a verification on blockchain
     */
    function recordVerification(
        bytes32 verificationHash,
        bytes32 profileHash,
        bool isVerified,
        string memory notes
    ) public {
        require(verificationHash != bytes32(0), "Invalid verification hash");
        require(profiles[profileHash].profileHash != bytes32(0), "Profile does not exist");
        
        Verification storage verification = verifications[verificationHash];
        verification.verificationHash = verificationHash;
        verification.verifier = msg.sender;
        verification.isVerified = isVerified;
        verification.timestamp = block.timestamp;
        verification.notes = notes;
        
        // Add to profile's verification history
        profiles[profileHash].verificationHashes.push(verificationHash);
        profiles[profileHash].lastModified = block.timestamp;
        
        emit VerificationRecorded(
            verificationHash,
            profileHash,
            msg.sender,
            isVerified,
            block.timestamp
        );
    }
    
    /**
     * @dev Add cryptographic signature to verification
     */
    function signVerification(
        bytes32 verificationHash,
        bytes memory signature
    ) public {
        require(
            verifications[verificationHash].verifier == msg.sender,
            "Only original verifier can sign"
        );
        
        verifications[verificationHash].signature = signature;
        
        emit VerificationSigned(verificationHash, msg.sender, block.timestamp);
    }
    
    /**
     * @dev Retrieve document information
     */
    function getDocument(bytes32 documentHash) 
        public 
        view 
        returns (Document memory) 
    {
        return documents[documentHash];
    }
    
    /**
     * @dev Retrieve verification history for a profile
     */
    function getVerificationHistory(bytes32 profileHash) 
        public 
        view 
        returns (bytes32[] memory) 
    {
        return profiles[profileHash].verificationHashes;
    }
    
    /**
     * @dev Verify a verification signature
     */
    function verifySignature(
        bytes32 verificationHash,
        address verifier
    ) public view returns (bool) {
        return verifications[verificationHash].verifier == verifier;
    }
    
    /**
     * @dev Get user's profiles
     */
    function getUserProfiles(address user) 
        public 
        view 
        returns (bytes32[] memory) 
    {
        return userProfiles[user];
    }
}
