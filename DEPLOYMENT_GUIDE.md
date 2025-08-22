# Medical Chatbot - Deployment Guide

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Local Development Setup](#local-development-setup)
3. [Docker Deployment](#docker-deployment)
4. [AWS Cloud Deployment](#aws-cloud-deployment)
5. [CI/CD Pipeline Setup](#cicd-pipeline-setup)
6. [Environment Configuration](#environment-configuration)
7. [Monitoring and Maintenance](#monitoring-and-maintenance)
8. [Troubleshooting](#troubleshooting)

## Prerequisites

### Required Accounts and Services
- [GitHub Account](https://github.com) - For code repository
- [OpenAI Account](https://platform.openai.com) - For GPT-4o API access
- [Pinecone Account](https://www.pinecone.io) - For vector database
- [AWS Account](https://aws.amazon.com) - For cloud deployment
- [Docker Hub Account](https://hub.docker.com) - Optional, for custom images

### Required Software
- Python 3.10+
- Git 2.25+
- Docker 20.10+
- AWS CLI 2.0+
- Conda/Miniconda (recommended)

### API Keys Required
- OpenAI API Key (with GPT-4o access)
- Pinecone API Key
- AWS Access Key ID and Secret Access Key

## Local Development Setup

### Step 1: Clone Repository

```bash
# Clone the repository
git clone https://github.com/entbappy/Build-a-Complete-Medical-Chatbot-with-LLMs-LangChain-Pinecone-Flask-AWS.git

# Navigate to project directory
cd Medical_Chatbot_LLMs_LangChain_Pinecone_Flask_AWS
```

### Step 2: Environment Setup

```bash
# Create conda environment
conda create -n medibot python=3.10 -y

# Activate environment
conda activate medibot

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Environment Configuration

Create `.env` file in the project root:

```bash
# Create .env file
touch .env

# Add the following content to .env
cat > .env << EOF
PINECONE_API_KEY="your_pinecone_api_key_here"
OPENAI_API_KEY="your_openai_api_key_here"
EOF
```

### Step 4: Initialize Vector Database

```bash
# Run the indexing script to populate Pinecone
python store_index.py
```

Expected output:
```
Loading PDFs from data/ directory...
Filtering documents...
Splitting text into chunks...
Generating embeddings...
Creating Pinecone index...
Storing vectors in Pinecone...
✅ Vector database initialized successfully!
```

### Step 5: Run Application

```bash
# Start the Flask application
python app.py
```

Expected output:
```
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:8080
 * Running on http://[your-ip]:8080
```

### Step 6: Test Application

Open your browser and navigate to `http://localhost:8080`

Test with sample queries:
- "What are the symptoms of diabetes?"
- "How is hypertension treated?"
- "What causes heart disease?"

## Docker Deployment

### Step 1: Create Dockerfile

```dockerfile
# Create Dockerfile in project root
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/ || exit 1

# Run application
CMD ["python", "app.py"]
```

### Step 2: Create Docker Compose (Optional)

```yaml
# docker-compose.yml
version: '3.8'

services:
  medical-chatbot:
    build: .
    ports:
      - "8080:8080"
    environment:
      - PINECONE_API_KEY=${PINECONE_API_KEY}
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    volumes:
      - ./data:/app/data:ro
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

### Step 3: Build and Run

```bash
# Build Docker image
docker build -t medical-chatbot:latest .

# Run with environment variables
docker run -d \
  --name medical-chatbot \
  -p 8080:8080 \
  -e PINECONE_API_KEY="your_pinecone_api_key" \
  -e OPENAI_API_KEY="your_openai_api_key" \
  medical-chatbot:latest

# Or use docker-compose
docker-compose up -d
```

### Step 4: Verify Deployment

```bash
# Check container status
docker ps

# View logs
docker logs medical-chatbot

# Test health check
curl http://localhost:8080/
```

## AWS Cloud Deployment

### Step 1: AWS Account Setup

#### Create IAM User for Deployment

1. Go to AWS Console → IAM → Users
2. Create new user: `medical-chatbot-deploy`
3. Attach policies:
   - `AmazonEC2ContainerRegistryFullAccess`
   - `AmazonEC2FullAccess`
4. Generate Access Key and Secret Key

#### Create ECR Repository

```bash
# Configure AWS CLI
aws configure

# Create ECR repository
aws ecr create-repository \
  --repository-name medical-chatbot \
  --region us-east-1

# Get login token
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin \
  <account-id>.dkr.ecr.us-east-1.amazonaws.com
```

### Step 2: EC2 Instance Setup

#### Launch EC2 Instance

1. Go to AWS Console → EC2 → Launch Instance
2. Choose Ubuntu 20.04 LTS AMI
3. Instance type: t3.medium (minimum)
4. Configure Security Group:
   - SSH (22) from your IP
   - HTTP (8080) from anywhere
5. Create or select key pair
6. Launch instance

#### Install Docker on EC2

```bash
# SSH into EC2 instance
ssh -i your-key.pem ubuntu@your-ec2-ip

# Update system
sudo apt-get update -y
sudo apt-get upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add user to docker group
sudo usermod -aG docker ubuntu
newgrp docker

# Install AWS CLI
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

# Configure AWS CLI
aws configure
```

### Step 3: Deploy to EC2

#### Push Image to ECR

```bash
# Tag image for ECR
docker tag medical-chatbot:latest \
  <account-id>.dkr.ecr.us-east-1.amazonaws.com/medical-chatbot:latest

# Push to ECR
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/medical-chatbot:latest
```

#### Deploy on EC2

```bash
# SSH into EC2
ssh -i your-key.pem ubuntu@your-ec2-ip

# Login to ECR
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin \
  <account-id>.dkr.ecr.us-east-1.amazonaws.com

# Pull and run image
docker run -d \
  --name medical-chatbot \
  --restart unless-stopped \
  -p 8080:8080 \
  -e PINECONE_API_KEY="your_pinecone_api_key" \
  -e OPENAI_API_KEY="your_openai_api_key" \
  <account-id>.dkr.ecr.us-east-1.amazonaws.com/medical-chatbot:latest
```

### Step 4: Configure Domain (Optional)

#### Using Route 53

1. Register domain or use existing
2. Create hosted zone
3. Create A record pointing to EC2 public IP
4. Configure SSL with Let's Encrypt (recommended)

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Get SSL certificate
sudo certbot --nginx -d your-domain.com
```

## CI/CD Pipeline Setup

### Step 1: GitHub Secrets Configuration

Go to GitHub Repository → Settings → Secrets and Variables → Actions

Add the following secrets:
```
AWS_ACCESS_KEY_ID: Your AWS access key
AWS_SECRET_ACCESS_KEY: Your AWS secret key
AWS_DEFAULT_REGION: us-east-1
ECR_REPO: <account-id>.dkr.ecr.us-east-1.amazonaws.com/medical-chatbot
PINECONE_API_KEY: Your Pinecone API key
OPENAI_API_KEY: Your OpenAI API key
EC2_HOST: Your EC2 public IP
EC2_USER: ubuntu
EC2_KEY: Your EC2 private key (base64 encoded)
```

### Step 2: Create GitHub Actions Workflow

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy Medical Chatbot

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v3
      with:
        python-version: '3.10'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        # Add your tests here
        python -c "import src.helper; print('Import test passed')"

  build-and-deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v3

    - name: Configure AWS credentials
      uses: aws-actions/configure-aws-credentials@v1
      with:
        aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
        aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        aws-region: ${{ secrets.AWS_DEFAULT_REGION }}

    - name: Login to Amazon ECR
      id: login-ecr
      uses: aws-actions/amazon-ecr-login@v1

    - name: Build, tag, and push image to Amazon ECR
      env:
        ECR_REGISTRY: ${{ steps.login-ecr.outputs.registry }}
        ECR_REPOSITORY: medical-chatbot
        IMAGE_TAG: ${{ github.sha }}
      run: |
        docker build -t $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG .
        docker build -t $ECR_REGISTRY/$ECR_REPOSITORY:latest .
        docker push $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG
        docker push $ECR_REGISTRY/$ECR_REPOSITORY:latest

    - name: Deploy to EC2
      uses: appleboy/ssh-action@v0.1.5
      with:
        host: ${{ secrets.EC2_HOST }}
        username: ${{ secrets.EC2_USER }}
        key: ${{ secrets.EC2_KEY }}
        script: |
          # Login to ECR
          aws ecr get-login-password --region ${{ secrets.AWS_DEFAULT_REGION }} | \
            docker login --username AWS --password-stdin ${{ secrets.ECR_REPO }}
          
          # Stop existing container
          docker stop medical-chatbot || true
          docker rm medical-chatbot || true
          
          # Pull and run new image
          docker pull ${{ secrets.ECR_REPO }}:latest
          docker run -d \
            --name medical-chatbot \
            --restart unless-stopped \
            -p 8080:8080 \
            -e PINECONE_API_KEY="${{ secrets.PINECONE_API_KEY }}" \
            -e OPENAI_API_KEY="${{ secrets.OPENAI_API_KEY }}" \
            ${{ secrets.ECR_REPO }}:latest
          
          # Clean up old images
          docker image prune -f
```

### Step 3: Configure EC2 as Self-Hosted Runner (Optional)

```bash
# On EC2 instance, install GitHub Actions runner
mkdir actions-runner && cd actions-runner

# Download runner
curl -o actions-runner-linux-x64-2.311.0.tar.gz -L \
  https://github.com/actions/runner/releases/download/v2.311.0/actions-runner-linux-x64-2.311.0.tar.gz

# Extract
tar xzf ./actions-runner-linux-x64-2.311.0.tar.gz

# Configure (follow GitHub instructions)
./config.sh --url https://github.com/your-username/your-repo --token YOUR_TOKEN

# Install as service
sudo ./svc.sh install
sudo ./svc.sh start
```

## Environment Configuration

### Development Environment

```bash
# .env.development
FLASK_ENV=development
FLASK_DEBUG=True
PINECONE_API_KEY="dev_pinecone_key"
OPENAI_API_KEY="dev_openai_key"
LOG_LEVEL=DEBUG
```

### Production Environment

```bash
# .env.production
FLASK_ENV=production
FLASK_DEBUG=False
PINECONE_API_KEY="prod_pinecone_key"
OPENAI_API_KEY="prod_openai_key"
LOG_LEVEL=INFO
```

### Environment Variables Reference

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `PINECONE_API_KEY` | Pinecone API key | Yes | None |
| `OPENAI_API_KEY` | OpenAI API key | Yes | None |
| `FLASK_ENV` | Flask environment | No | production |
| `FLASK_DEBUG` | Debug mode | No | False |
| `LOG_LEVEL` | Logging level | No | INFO |
| `PORT` | Application port | No | 8080 |

## Monitoring and Maintenance

### Health Checks

Create health check endpoint in `app.py`:

```python
@app.route('/health')
def health_check():
    try:
        # Test Pinecone connection
        docsearch.similarity_search("test", k=1)
        return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}, 500
```

### Logging Configuration

```python
import logging
from logging.handlers import RotatingFileHandler

if not app.debug:
    file_handler = RotatingFileHandler('logs/medical_chatbot.log', 
                                     maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
```

### Monitoring Script

```bash
#!/bin/bash
# monitor.sh - Simple monitoring script

# Check if container is running
if ! docker ps | grep -q medical-chatbot; then
    echo "Container not running, restarting..."
    docker start medical-chatbot
fi

# Check health endpoint
if ! curl -f http://localhost:8080/health; then
    echo "Health check failed, restarting container..."
    docker restart medical-chatbot
fi

# Check disk space
DISK_USAGE=$(df / | tail -1 | awk '{print $5}' | sed 's/%//')
if [ $DISK_USAGE -gt 80 ]; then
    echo "Disk usage high: ${DISK_USAGE}%"
    # Clean up old Docker images
    docker image prune -f
fi
```

### Backup Strategy

```bash
#!/bin/bash
# backup.sh - Backup script

# Backup application data
tar -czf backup_$(date +%Y%m%d_%H%M%S).tar.gz \
  --exclude='*.pyc' \
  --exclude='__pycache__' \
  --exclude='.git' \
  .

# Upload to S3 (optional)
aws s3 cp backup_*.tar.gz s3://your-backup-bucket/medical-chatbot/
```

## Troubleshooting

### Common Issues

#### 1. Container Won't Start

```bash
# Check logs
docker logs medical-chatbot

# Common causes:
# - Missing environment variables
# - Port already in use
# - Insufficient memory

# Solutions:
docker run --env-file .env medical-chatbot:latest
sudo netstat -tulpn | grep :8080
docker stats
```

#### 2. API Connection Issues

```bash
# Test OpenAI connection
curl -H "Authorization: Bearer $OPENAI_API_KEY" \
  https://api.openai.com/v1/models

# Test Pinecone connection
curl -H "Api-Key: $PINECONE_API_KEY" \
  https://api.pinecone.io/indexes
```

#### 3. Performance Issues

```bash
# Monitor resource usage
docker stats medical-chatbot

# Check application logs
docker logs -f medical-chatbot

# Optimize if needed:
# - Increase container memory
# - Scale horizontally
# - Implement caching
```

#### 4. Deployment Failures

```bash
# Check GitHub Actions logs
# Verify AWS credentials
aws sts get-caller-identity

# Check EC2 connectivity
ssh -i your-key.pem ubuntu@your-ec2-ip

# Verify ECR access
aws ecr describe-repositories
```

### Debug Mode

Enable debug mode for troubleshooting:

```python
# In app.py
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
```

### Log Analysis

```bash
# View recent logs
docker logs --tail 100 medical-chatbot

# Follow logs in real-time
docker logs -f medical-chatbot

# Search for errors
docker logs medical-chatbot 2>&1 | grep -i error
```

## Security Checklist

- [ ] API keys stored in environment variables
- [ ] No sensitive data in source code
- [ ] HTTPS enabled in production
- [ ] Security groups properly configured
- [ ] Regular security updates applied
- [ ] Container running as non-root user
- [ ] Firewall rules configured
- [ ] Access logs monitored

## Performance Optimization

### Application Level
- Implement response caching
- Use connection pooling
- Optimize vector search parameters
- Add request rate limiting

### Infrastructure Level
- Use load balancer for multiple instances
- Implement auto-scaling
- Use CDN for static assets
- Optimize Docker image size

### Database Level
- Monitor Pinecone performance
- Optimize chunk size and overlap
- Consider index optimization
- Implement query caching

---

## Support

For deployment issues or questions:
1. Check the troubleshooting section
2. Review application logs
3. Consult the technical specifications
4. Contact the development team

**Last Updated**: January 2025
**Guide Version**: 1.0.0