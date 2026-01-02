# Blockchain Configuration

This directory contains the smart contracts and blockchain integration for the School Identity Vault.

## Smart Contracts

### VerificationRecord.sol
Main smart contract for recording educational document verifications on blockchain.

**Key Features:**
- Store document hashes (not full documents)
- Record verification signatures
- Maintain immutable audit trail
- Enable cryptographic verification

## Deployment

```bash
# Compile contract
solc --optimize --bin --abi contracts/VerificationRecord.sol

# Deploy to network
# See DEPLOYMENT.md for detailed instructions
```

## Network Configuration

- **Development**: Ganache (localhost:8545)
- **Testnet**: Sepolia / Goerli
- **Mainnet**: Azure Blockchain Workbench
- **Permissioned**: Hyperledger Fabric (for UNICEF partnership)

## Contract Addresses

Add deployed contract addresses here:

- **Development**: 0x...
- **Testnet**: 0x...
- **Mainnet**: 0x...
