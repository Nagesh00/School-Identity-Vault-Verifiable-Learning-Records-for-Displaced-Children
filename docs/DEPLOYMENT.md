# Deployment Guide

## Prerequisites

- Azure Account with services enabled:
  - Azure Container Registry
  - Azure App Service
  - Azure Database for PostgreSQL
  - Azure Cosmos DB
  - Azure Cognitive Services
  - Azure OpenAI
- Docker installed
- Node.js 16+ installed
- Python 3.9+ installed

## Local Development Setup

### 1. Clone Repository
```bash
git clone https://github.com/Nagesh00/School-Identity-Vault-Verifiable-Learning-Records-for-Displaced-Children.git
cd School-Identity-Vault-Verifiable-Learning-Records-for-Displaced-Children
```

### 2. Backend Setup
```bash
cd backend
npm install
cp ../.env.example .env

# Update .env with your credentials
nano .env

# Start development server
npm run dev
```

### 3. Frontend Setup
```bash
cd frontend
npm install
npm start
# Runs at http://localhost:3000
```

### 4. ML Engine Setup
```bash
cd ml-engine
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Update .env with Azure credentials
nano .env

# Start ML service
python -m uvicorn src.main:app --reload --port 8000
```

## Azure Deployment

### 1. Create Azure Resources

```bash
# Login to Azure
az login

# Create Resource Group
az group create \
  --name school-identity-vault-rg \
  --location eastus

# Create App Service Plan
az appservice plan create \
  --name school-identity-vault-plan \
  --resource-group school-identity-vault-rg \
  --sku B2

# Create Web App for Backend
az webapp create \
  --resource-group school-identity-vault-rg \
  --plan school-identity-vault-plan \
  --name school-identity-vault-api \
  --runtime "node|18-lts"

# Create App Service for ML Engine
az webapp create \
  --resource-group school-identity-vault-rg \
  --plan school-identity-vault-plan \
  --name school-identity-vault-ml \
  --runtime "python|3.9"

# Create PostgreSQL Database
az postgres server create \
  --resource-group school-identity-vault-rg \
  --name school-identity-vault-db \
  --location eastus \
  --admin-user dbadmin \
  --admin-password YourPassword123! \
  --sku-name B_Gen5_1 \
  --storage-size 51200

# Create Storage Account
az storage account create \
  --name schoolidentityvault \
  --resource-group school-identity-vault-rg \
  --location eastus

# Create Container Registry
az acr create \
  --resource-group school-identity-vault-rg \
  --name schoolidentityacr \
  --sku Basic
```

### 2. Configure Azure Cognitive Services

```bash
# Create Computer Vision account
az cognitiveservices account create \
  --name school-identity-vision \
  --resource-group school-identity-vault-rg \
  --kind ComputerVision \
  --sku S1 \
  --location eastus

# Create Language Service
az cognitiveservices account create \
  --name school-identity-language \
  --resource-group school-identity-vault-rg \
  --kind TextAnalytics \
  --sku S \
  --location eastus

# Create OpenAI Service
az cognitiveservices account create \
  --name school-identity-openai \
  --resource-group school-identity-vault-rg \
  --kind OpenAI \
  --sku S0 \
  --location eastus
```

### 3. Containerize Applications

```bash
# Build Backend Image
cd backend
docker build -t schoolidentityacr.azurecr.io/backend:latest .
docker push schoolidentityacr.azurecr.io/backend:latest

# Build ML Engine Image
cd ../ml-engine
docker build -t schoolidentityacr.azurecr.io/ml-engine:latest .
docker push schoolidentityacr.azurecr.io/ml-engine:latest

# Build Frontend Image
cd ../frontend
docker build -t schoolidentityacr.azurecr.io/frontend:latest .
docker push schoolidentityacr.azurecr.io/frontend:latest
```

### 4. Deploy to App Service

```bash
# Deploy Backend
az webapp deployment container config \
  --resource-group school-identity-vault-rg \
  --name school-identity-vault-api \
  --enable-cd true

az webapp create \
  --resource-group school-identity-vault-rg \
  --plan school-identity-vault-plan \
  --name school-identity-vault-api \
  --deployment-container-image-name schoolidentityacr.azurecr.io/backend:latest

# Deploy ML Engine
az webapp create \
  --resource-group school-identity-vault-rg \
  --plan school-identity-vault-plan \
  --name school-identity-vault-ml \
  --deployment-container-image-name schoolidentityacr.azurecr.io/ml-engine:latest
```

### 5. Configure Environment Variables

```bash
# For Backend API
az webapp config appsettings set \
  --resource-group school-identity-vault-rg \
  --name school-identity-vault-api \
  --settings \
    AZURE_VISION_KEY="<your-key>" \
    AZURE_OPENAI_KEY="<your-key>" \
    DB_HOST="school-identity-vault-db.postgres.database.azure.com" \
    DB_USER="dbadmin@school-identity-vault-db" \
    DB_PASSWORD="<your-password>" \
    NODE_ENV="production"
```

## Docker Compose Local Deployment

```bash
# Create docker-compose.yml in root
docker-compose up -d

# Access:
# Frontend: http://localhost:3000
# Backend: http://localhost:5000
# ML Engine: http://localhost:8000
```

## Kubernetes Deployment (Optional)

Create `k8s-deployment.yaml`:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: school-identity-vault-backend
  labels:
    app: backend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: backend
  template:
    metadata:
      labels:
        app: backend
    spec:
      containers:
      - name: backend
        image: schoolidentityacr.azurecr.io/backend:latest
        ports:
        - containerPort: 5000
        env:
        - name: AZURE_VISION_KEY
          valueFrom:
            secretKeyRef:
              name: azure-credentials
              key: vision-key
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
```

```bash
# Deploy to AKS
kubectl apply -f k8s-deployment.yaml
```

## Database Migration

```bash
# Install migration tool
npm install -g flyway-cli

# Run migrations
flyway -url=jdbc:postgresql://host:5432/school_identity_vault \
       -user=dbadmin \
       -password=YourPassword123! \
       migrate
```

## SSL/TLS Certificate

```bash
# Generate self-signed certificate (development)
openssl req -x509 -newkey rsa:4096 -nodes \
  -out cert.pem -keyout key.pem -days 365

# For production, use Azure Key Vault or Let's Encrypt
```

## Monitoring & Logging

### Azure Application Insights

```bash
# Create Application Insights
az monitor app-insights component create \
  --app school-identity-vault-insights \
  --location eastus \
  --resource-group school-identity-vault-rg \
  --application-type web

# Configure in backend .env
APPINSIGHTS_INSTRUMENTATION_KEY="<key>"
```

### View Logs

```bash
# Stream logs
az webapp log tail \
  --resource-group school-identity-vault-rg \
  --name school-identity-vault-api

# Download logs
az webapp log download \
  --resource-group school-identity-vault-rg \
  --name school-identity-vault-api \
  --log-file logs.zip
```

## Health Checks

```bash
# Test backend
curl http://localhost:5000/api/health

# Test ML engine
curl http://localhost:8000/health

# Test frontend
curl http://localhost:3000
```

## Scaling

```bash
# Scale App Service plan
az appservice plan update \
  --name school-identity-vault-plan \
  --resource-group school-identity-vault-rg \
  --sku B3

# Auto-scale
az monitor autoscale create \
  --name school-identity-vault-autoscale \
  --resource-group school-identity-vault-rg \
  --resource-type "Microsoft.Web/serverfarms" \
  --resource school-identity-vault-plan \
  --min-count 2 \
  --max-count 10 \
  --count 3
```
