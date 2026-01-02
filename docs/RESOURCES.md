# Resource Index

## Quick Links

### 📖 Documentation
- [README.md](../README.md) - Project overview
- [QUICKSTART.md](../QUICKSTART.md) - Getting started in 5 minutes
- [PROJECT_SETUP_COMPLETE.md](../PROJECT_SETUP_COMPLETE.md) - Setup summary
- [IMPLEMENTATION_CHECKLIST.md](../IMPLEMENTATION_CHECKLIST.md) - Development tasks

### 🏗️ Architecture & Design
- [ARCHITECTURE.md](./ARCHITECTURE.md) - System design & components
- [API.md](./API.md) - API endpoints & examples
- [DEPLOYMENT.md](./DEPLOYMENT.md) - Azure deployment guide

### 💻 Source Code

#### Backend API
- [backend/src/index.js](../backend/src/index.js) - Application entry point
- [backend/src/routes/documents.js](../backend/src/routes/documents.js) - Document endpoints
- [backend/src/routes/profiles.js](../backend/src/routes/profiles.js) - Profile endpoints
- [backend/src/routes/verification.js](../backend/src/routes/verification.js) - Verification endpoints
- [backend/src/routes/health.js](../backend/src/routes/health.js) - Health check
- [backend/src/services/documentService.js](../backend/src/services/documentService.js) - Document logic
- [backend/src/services/profileService.js](../backend/src/services/profileService.js) - Profile logic
- [backend/src/services/verificationService.js](../backend/src/services/verificationService.js) - Verification logic
- [backend/package.json](../backend/package.json) - Node dependencies

#### Frontend Application
- [frontend/src/App.tsx](../frontend/src/App.tsx) - Main app component
- [frontend/src/components/DocumentUpload.tsx](../frontend/src/components/DocumentUpload.tsx) - Upload component
- [frontend/src/components/LearningProfileSummary.tsx](../frontend/src/components/LearningProfileSummary.tsx) - Profile display
- [frontend/src/components/VerificationPanel.tsx](../frontend/src/components/VerificationPanel.tsx) - Verification UI
- [frontend/src/services/apiClient.ts](../frontend/src/services/apiClient.ts) - API integration
- [frontend/package.json](../frontend/package.json) - React dependencies

#### ML Engine
- [ml-engine/src/main.py](../ml-engine/src/main.py) - FastAPI server
- [ml-engine/src/document_processor.py](../ml-engine/src/document_processor.py) - OCR & text extraction
- [ml-engine/src/profile_reconstructor.py](../ml-engine/src/profile_reconstructor.py) - Profile building
- [ml-engine/src/confidence_scorer.py](../ml-engine/src/confidence_scorer.py) - Confidence estimation
- [ml-engine/requirements.txt](../ml-engine/requirements.txt) - Python dependencies

#### Blockchain
- [blockchain/contracts/VerificationRecord.sol](../blockchain/contracts/VerificationRecord.sol) - Smart contract
- [blockchain/services/blockchain_service.py](../blockchain/services/blockchain_service.py) - Blockchain integration
- [blockchain/README.md](../blockchain/README.md) - Blockchain documentation

### 🔧 Configuration
- [docker-compose.yml](../docker-compose.yml) - Multi-container setup
- [backend/Dockerfile](../backend/Dockerfile) - Backend container
- [frontend/Dockerfile](../frontend/Dockerfile) - Frontend container
- [frontend/nginx.conf](../frontend/nginx.conf) - Web server config
- [ml-engine/Dockerfile](../ml-engine/Dockerfile) - ML Engine container
- [.env.example](../.env.example) - Environment template
- [.gitignore](../.gitignore) - Git exclusions
- [backend/.gitignore](../backend/.gitignore) - Backend exclusions

### 📋 Project Files
- [package.json](../package.json) - Monorepo scripts
- [LICENSE](../LICENSE) - MIT License
- [CONTRIBUTING.md](../CONTRIBUTING.md) - Contribution guidelines

---

## API Reference

### Base URL
```
http://localhost:5000/api
```

### Endpoints Summary

| Method | Path | Description |
|--------|------|-------------|
| GET | /health | Health check |
| POST | /documents/upload | Upload document |
| GET | /documents/:id | Get document |
| POST | /profiles | Create profile |
| GET | /profiles/:id | Get profile |
| PUT | /profiles/:id | Update profile |
| POST | /profiles/:id/merge | Merge documents |
| POST | /verification/verify | Submit verification |
| POST | /verification/:id/sign | Sign verification |
| GET | /verification/:id/history | Get audit trail |
| POST | /verification/:id/blockchain | Record on blockchain |

See [docs/API.md](./API.md) for complete documentation.

---

## Key Concepts

### Document Processing Pipeline
1. User uploads image/PDF
2. Azure Computer Vision extracts text (OCR)
3. Azure Language Service parses structure
4. Data is normalized to standard format
5. Confidence scores calculated
6. Document hash recorded on blockchain

### Profile Reconstruction Flow
1. Collect documents from multiple sources
2. Merge data with conflict resolution
3. Generate standardized profile summary
4. Map to local curriculum equivalence
5. Calculate overall confidence score
6. Store profile hash on blockchain

### Verification Workflow
1. School/agency reviews profile
2. Submits verification decision
3. Cryptographic signature added
4. Recorded on blockchain
5. Verification history maintained
6. Proof available to other institutions

---

## Technology Stack Reference

### Backend
- **Runtime**: Node.js 18+
- **Framework**: Express.js 4.18+
- **Authentication**: JWT / OAuth2
- **Database**: PostgreSQL 15
- **ORM**: Sequelize
- **Testing**: Jest

### Frontend
- **Framework**: React 18+
- **Language**: TypeScript 5+
- **State Management**: Zustand
- **HTTP Client**: Axios
- **Styling**: Tailwind CSS
- **Testing**: React Testing Library

### ML Engine
- **Runtime**: Python 3.9+
- **Framework**: FastAPI
- **ML Libraries**: scikit-learn, pandas, numpy
- **Azure Services**: Computer Vision, Language, OpenAI
- **Testing**: pytest

### Blockchain
- **Language**: Solidity 0.8+
- **Framework**: Web3.js
- **Network**: Ethereum-compatible (Hyperledger Fabric ready)
- **Standards**: ERC-20, ERC-721 ready

### Infrastructure
- **Containerization**: Docker
- **Orchestration**: Docker Compose (Kubernetes ready)
- **Cloud**: Microsoft Azure
- **CI/CD**: GitHub Actions (configured)
- **Monitoring**: Azure Application Insights

---

## Development Guides

### Getting Started
1. Read [QUICKSTART.md](../QUICKSTART.md)
2. Review [ARCHITECTURE.md](./ARCHITECTURE.md)
3. Explore [API.md](./API.md)
4. Follow setup instructions

### Making Changes
1. Create feature branch: `git checkout -b feature/name`
2. Make changes following style guidelines
3. Add tests for new functionality
4. Update documentation
5. Create pull request with clear message

See [CONTRIBUTING.md](../CONTRIBUTING.md) for detailed guidelines.

### Deploying to Production
1. Follow [DEPLOYMENT.md](./DEPLOYMENT.md)
2. Set up Azure resources
3. Configure environment variables
4. Run tests and security checks
5. Deploy to staging
6. Deploy to production
7. Monitor with Application Insights

---

## Important Files Checklist

### Must Read
- [ ] [README.md](../README.md) - Project overview
- [ ] [QUICKSTART.md](../QUICKSTART.md) - Get running quickly
- [ ] [ARCHITECTURE.md](./ARCHITECTURE.md) - Understand design

### Configuration
- [ ] [.env.example](../.env.example) - Environment setup
- [ ] [docker-compose.yml](../docker-compose.yml) - Local development
- [ ] [DEPLOYMENT.md](./DEPLOYMENT.md) - Production setup

### Source Code Entry Points
- [ ] [backend/src/index.js](../backend/src/index.js) - API server
- [ ] [frontend/src/App.tsx](../frontend/src/App.tsx) - Frontend app
- [ ] [ml-engine/src/main.py](../ml-engine/src/main.py) - ML server

### Contributing
- [ ] [CONTRIBUTING.md](../CONTRIBUTING.md) - Development guidelines
- [ ] [IMPLEMENTATION_CHECKLIST.md](../IMPLEMENTATION_CHECKLIST.md) - Tasks list

---

## Common Commands

### Development
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Backend tests
cd backend && npm test

# Frontend tests
cd frontend && npm test

# ML Engine tests
cd ml-engine && pytest
```

### Deployment
```bash
# Build images
docker-compose build

# Push to registry
docker push <image>

# Deploy to Azure
az webapp create ...
```

---

## Support Resources

### Documentation
- Architecture: [ARCHITECTURE.md](./ARCHITECTURE.md)
- API Reference: [API.md](./API.md)
- Deployment: [DEPLOYMENT.md](./DEPLOYMENT.md)
- Contributing: [CONTRIBUTING.md](../CONTRIBUTING.md)

### External Resources
- [Express.js Docs](https://expressjs.com/)
- [React Docs](https://react.dev/)
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Solidity Docs](https://docs.soliditylang.org/)
- [Azure Docs](https://docs.microsoft.com/azure/)
- [Docker Docs](https://docs.docker.com/)

### GitHub Issues & Discussions
- Report bugs: Use GitHub Issues
- Ask questions: Use GitHub Discussions
- Suggest features: Use GitHub Issues with "enhancement" label

---

## Project Statistics

| Metric | Value |
|--------|-------|
| Total Files | 35+ |
| Lines of Code | 3,000+ |
| Components | 20+ |
| API Endpoints | 9 |
| Documentation Pages | 7 |
| Docker Services | 5 |
| Supported Languages | 5+ |

---

## Last Updated

January 2, 2025

---

**Next Step**: Start with [QUICKSTART.md](../QUICKSTART.md) to get the system running!
