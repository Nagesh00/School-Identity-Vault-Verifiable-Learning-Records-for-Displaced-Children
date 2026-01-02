# Getting Started - Quick Start Guide

## Prerequisites

- Git
- Docker & Docker Compose (recommended) OR
- Node.js 16+
- Python 3.9+
- Azure Account (for AI services)

## Option 1: Docker (Recommended)

### 1. Setup Environment
```bash
cp .env.example .env
# Edit .env with your Azure credentials
```

### 2. Start All Services
```bash
docker-compose up -d
```

### 3. Access Applications
- Frontend: http://localhost:3000
- Backend API: http://localhost:5000/api
- ML Engine: http://localhost:8000
- Database: localhost:5432

### 4. Test Health Endpoints
```bash
curl http://localhost:5000/api/health
curl http://localhost:8000/health
```

## Option 2: Manual Setup

### 1. Backend Setup
```bash
cd backend
npm install
cp ../.env.example .env
# Edit .env with Azure credentials
npm run dev
# Runs on http://localhost:5000
```

### 2. Frontend Setup (new terminal)
```bash
cd frontend
npm install
npm start
# Runs on http://localhost:3000
```

### 3. ML Engine Setup (new terminal)
```bash
cd ml-engine
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m uvicorn src.main:app --reload
# Runs on http://localhost:8000
```

## Demo Workflow

### 1. Upload Document
```bash
curl -X POST http://localhost:5000/api/documents/upload \
  -F "file=@sample_document.jpg" \
  -F "documentType=report_card" \
  -F "childId=child_001" \
  -F "sourceCountry=Syria"
```

### 2. Create Profile
Copy the returned `documentId` and run:
```bash
curl -X POST http://localhost:5000/api/profiles \
  -H "Content-Type: application/json" \
  -d '{
    "childName": "Ahmed Hassan",
    "childId": "child_001",
    "documentIds": ["<returned-document-id>"],
    "sourceCountry": "Syria"
  }'
```

### 3. Verify Profile
Copy the returned `profileId` and run:
```bash
curl -X POST http://localhost:5000/api/verification/verify \
  -H "Content-Type: application/json" \
  -d '{
    "profileId": "<profile-id>",
    "schoolId": "school_001",
    "schoolName": "Local School",
    "isVerified": true,
    "verificationNotes": "Profile verified against school records"
  }'
```

### 4. View Verification History
```bash
curl http://localhost:5000/api/verification/<profile-id>/history
```

## Project Structure

```
school-identity-vault/
├── backend/              # Node.js REST API
├── frontend/             # React web application
├── ml-engine/            # Python AI/ML services
├── blockchain/           # Smart contracts & blockchain integration
├── docs/                 # Full documentation
├── docker-compose.yml    # Docker setup
└── README.md             # This file
```

## Key Files

- [README.md](README.md) - Project overview
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) - System design
- [docs/API.md](docs/API.md) - API endpoints
- [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) - Deployment guide
- [CONTRIBUTING.md](CONTRIBUTING.md) - Contribution guidelines

## Troubleshooting

### Port Already in Use
```bash
# Find process using port
lsof -i :5000

# Kill process
kill -9 <PID>
```

### Database Connection Error
Ensure PostgreSQL is running:
```bash
docker ps  # Check if postgres container is running
```

### Azure Credentials Error
- Verify .env file has correct credentials
- Check Azure resource names match
- Ensure services are enabled in Azure subscription

## Support

- 📖 See [docs/](docs/) for detailed documentation
- 🐛 Report issues on GitHub
- 💬 Discuss ideas in GitHub Discussions

## License

MIT - See [LICENSE](LICENSE)

## Next Steps

1. Read [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for system design
2. Review [docs/API.md](docs/API.md) for API endpoints
3. Check [CONTRIBUTING.md](CONTRIBUTING.md) to contribute
4. Follow [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) to deploy

---

**Mission**: Ensuring displaced children never lose their educational records again.
