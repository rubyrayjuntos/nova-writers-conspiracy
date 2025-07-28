# 🚀 Nova: Writers Conspiracy - Deployment Guide

## Overview

This guide provides comprehensive instructions for deploying the Nova Writers Conspiracy platform, from local development to production environments. The system uses Docker containers for consistency across environments and supports both single-server and distributed deployments.

## Prerequisites

### System Requirements

- **Operating System**: Linux (Ubuntu 20.04+ recommended), macOS, or Windows with WSL2
- **Docker**: Version 20.10+ with Docker Compose
- **Memory**: Minimum 8GB RAM (16GB recommended for production)
- **Storage**: 50GB+ available disk space
- **Network**: Stable internet connection for API calls

### Required Accounts and API Keys

- **OpenAI API**: GPT-4 access with sufficient credits
- **Pinecone**: Vector database account and API key
- **SerperDev**: Web search API account and key
- **PostgreSQL**: Database instance (local or cloud)
- **Redis**: Cache instance (local or cloud)

## Local Development Setup

### 1. Clone and Initialize

```bash
# Clone the repository
git clone https://github.com/rubyrayjuntos/nova-writers-conspiracy.git
cd nova-writers-conspiracy

# Install dependencies
cd frontend && npm install
cd ../backend && pip install -r requirements.txt
```

### 2. Environment Configuration

Create environment files for each service:

**Backend (.env)**
```bash
# Database Configuration
DATABASE_URL=postgresql://username:password@localhost:5432/nova_db
REDIS_URL=redis://localhost:6379

# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-4

# Pinecone Configuration
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_ENVIRONMENT=your_pinecone_environment
PINECONE_INDEX_NAME=nova_memory

# SerperDev Configuration
SERPER_API_KEY=your_serper_api_key

# JWT Configuration
JWT_SECRET=your_jwt_secret_key
JWT_ALGORITHM=HS256

# Application Configuration
DEBUG=True
LOG_LEVEL=DEBUG
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

**Frontend (.env)**
```bash
# API Configuration
VITE_API_BASE_URL=http://localhost:8000
VITE_WS_URL=ws://localhost:8000/ws

# Feature Flags
VITE_ENABLE_AGENT_CHAT=true
VITE_ENABLE_REAL_TIME=true
VITE_ENABLE_ILLUSTRATIONS=true
```

### 3. Database Setup

```bash
# Start PostgreSQL and Redis
docker-compose up -d postgres redis

# Run database migrations
cd backend
alembic upgrade head

# Create initial admin user
python scripts/create_admin.py
```

### 4. Start Development Servers

```bash
# Terminal 1: Backend API
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2: Frontend Development Server
cd frontend
npm run dev

# Terminal 3: Celery Worker (for background tasks)
cd backend
celery -A app.core.celery worker --loglevel=info

# Terminal 4: Celery Beat (for scheduled tasks)
cd backend
celery -A app.core.celery beat --loglevel=info
```

## Docker Deployment

### 1. Production Docker Compose

```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  # Frontend
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile.prod
    ports:
      - "80:80"
    environment:
      - VITE_API_BASE_URL=https://api.nova-writers.com
    depends_on:
      - backend
    restart: unless-stopped

  # Backend API
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile.prod
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://nova_user:nova_pass@postgres:5432/nova_db
      - REDIS_URL=redis://redis:6379
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - PINECONE_API_KEY=${PINECONE_API_KEY}
      - JWT_SECRET=${JWT_SECRET}
      - DEBUG=False
      - LOG_LEVEL=INFO
    depends_on:
      - postgres
      - redis
    restart: unless-stopped

  # Celery Worker
  celery_worker:
    build:
      context: ./backend
      dockerfile: Dockerfile.prod
    command: celery -A app.core.celery worker --loglevel=info
    environment:
      - DATABASE_URL=postgresql://nova_user:nova_pass@postgres:5432/nova_db
      - REDIS_URL=redis://redis:6379
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    depends_on:
      - postgres
      - redis
    restart: unless-stopped

  # Celery Beat
  celery_beat:
    build:
      context: ./backend
      dockerfile: Dockerfile.prod
    command: celery -A app.core.celery beat --loglevel=info
    environment:
      - DATABASE_URL=postgresql://nova_user:nova_pass@postgres:5432/nova_db
      - REDIS_URL=redis://redis:6379
    depends_on:
      - postgres
      - redis
    restart: unless-stopped

  # PostgreSQL Database
  postgres:
    image: postgres:15
    environment:
      - POSTGRES_DB=nova_db
      - POSTGRES_USER=nova_user
      - POSTGRES_PASSWORD=nova_pass
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    restart: unless-stopped

  # Redis Cache
  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data
    ports:
      - "6379:6379"
    restart: unless-stopped

  # Nginx Reverse Proxy
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - frontend
      - backend
    restart: unless-stopped

volumes:
  postgres_data:
  redis_data:
```

### 2. Production Dockerfiles

**Backend Dockerfile.prod**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd -m -u 1000 nova && chown -R nova:nova /app
USER nova

# Expose port
EXPOSE 8000

# Start application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Frontend Dockerfile.prod**
```dockerfile
FROM node:18-alpine as builder

WORKDIR /app

# Copy package files
COPY package*.json ./
RUN npm ci --only=production

# Copy source code
COPY . .

# Build application
RUN npm run build

# Production stage
FROM nginx:alpine

# Copy built application
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

### 3. Nginx Configuration

```nginx
# nginx.conf
events {
    worker_connections 1024;
}

http {
    upstream backend {
        server backend:8000;
    }

    upstream frontend {
        server frontend:80;
    }

    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
    limit_req_zone $binary_remote_addr zone=login:10m rate=5r/m;

    server {
        listen 80;
        server_name nova-writers.com;

        # Redirect to HTTPS
        return 301 https://$server_name$request_uri;
    }

    server {
        listen 443 ssl http2;
        server_name nova-writers.com;

        # SSL Configuration
        ssl_certificate /etc/nginx/ssl/cert.pem;
        ssl_certificate_key /etc/nginx/ssl/key.pem;
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384;
        ssl_prefer_server_ciphers off;

        # Security headers
        add_header X-Frame-Options DENY;
        add_header X-Content-Type-Options nosniff;
        add_header X-XSS-Protection "1; mode=block";
        add_header Strict-Transport-Security "max-age=31536000; includeSubDomains";

        # API routes
        location /api/ {
            limit_req zone=api burst=20 nodelay;
            
            proxy_pass http://backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            
            # WebSocket support
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
        }

        # Frontend routes
        location / {
            proxy_pass http://frontend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
}
```

## Cloud Deployment

### 1. AWS Deployment

**EC2 Setup**
```bash
# Launch EC2 instance
aws ec2 run-instances \
    --image-id ami-0c02fb55956c7d323 \
    --instance-type t3.large \
    --key-name nova-key \
    --security-group-ids sg-0123456789abcdef \
    --subnet-id subnet-0123456789abcdef

# Install Docker
sudo yum update -y
sudo yum install -y docker
sudo service docker start
sudo usermod -a -G docker ec2-user

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

**RDS PostgreSQL Setup**
```bash
# Create RDS instance
aws rds create-db-instance \
    --db-instance-identifier nova-postgres \
    --db-instance-class db.t3.micro \
    --engine postgres \
    --master-username nova_user \
    --master-user-password secure_password \
    --allocated-storage 20 \
    --vpc-security-group-ids sg-0123456789abcdef
```

**ElastiCache Redis Setup**
```bash
# Create Redis cluster
aws elasticache create-cache-cluster \
    --cache-cluster-id nova-redis \
    --engine redis \
    --cache-node-type cache.t3.micro \
    --num-cache-nodes 1 \
    --vpc-security-group-ids sg-0123456789abcdef
```

### 2. Google Cloud Platform

**Compute Engine Setup**
```bash
# Create VM instance
gcloud compute instances create nova-instance \
    --zone=us-central1-a \
    --machine-type=e2-standard-2 \
    --image-family=ubuntu-2004-lts \
    --image-project=ubuntu-os-cloud \
    --tags=http-server,https-server

# Install Docker
gcloud compute ssh nova-instance --zone=us-central1-a --command="
sudo apt-get update
sudo apt-get install -y docker.io docker-compose
sudo usermod -a -G docker $USER
"
```

**Cloud SQL Setup**
```bash
# Create PostgreSQL instance
gcloud sql instances create nova-postgres \
    --database-version=POSTGRES_15 \
    --tier=db-f1-micro \
    --region=us-central1 \
    --storage-type=SSD \
    --storage-size=10GB
```

### 3. Azure Deployment

**Virtual Machine Setup**
```bash
# Create VM
az vm create \
    --resource-group nova-rg \
    --name nova-vm \
    --image UbuntuLTS \
    --size Standard_B2s \
    --admin-username azureuser \
    --generate-ssh-keys

# Install Docker
az vm run-command invoke \
    --resource-group nova-rg \
    --name nova-vm \
    --command-id RunShellScript \
    --scripts "
    sudo apt-get update
    sudo apt-get install -y docker.io docker-compose
    sudo usermod -a -G docker azureuser
    "
```

## Kubernetes Deployment

### 1. Kubernetes Manifests

**namespace.yaml**
```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: nova-writers
```

**configmap.yaml**
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: nova-config
  namespace: nova-writers
data:
  DATABASE_URL: "postgresql://nova_user:nova_pass@nova-postgres:5432/nova_db"
  REDIS_URL: "redis://nova-redis:6379"
  DEBUG: "False"
  LOG_LEVEL: "INFO"
```

**secret.yaml**
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: nova-secrets
  namespace: nova-writers
type: Opaque
data:
  OPENAI_API_KEY: <base64-encoded-key>
  PINECONE_API_KEY: <base64-encoded-key>
  JWT_SECRET: <base64-encoded-secret>
```

**deployment.yaml**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nova-backend
  namespace: nova-writers
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nova-backend
  template:
    metadata:
      labels:
        app: nova-backend
    spec:
      containers:
      - name: backend
        image: nova-backend:latest
        ports:
        - containerPort: 8000
        envFrom:
        - configMapRef:
            name: nova-config
        - secretRef:
            name: nova-secrets
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
```

**service.yaml**
```yaml
apiVersion: v1
kind: Service
metadata:
  name: nova-backend-service
  namespace: nova-writers
spec:
  selector:
    app: nova-backend
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
  type: ClusterIP
```

**ingress.yaml**
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: nova-ingress
  namespace: nova-writers
  annotations:
    kubernetes.io/ingress.class: nginx
    cert-manager.io/cluster-issuer: letsencrypt-prod
spec:
  tls:
  - hosts:
    - nova-writers.com
    secretName: nova-tls
  rules:
  - host: nova-writers.com
    http:
      paths:
      - path: /api
        pathType: Prefix
        backend:
          service:
            name: nova-backend-service
            port:
              number: 80
      - path: /
        pathType: Prefix
        backend:
          service:
            name: nova-frontend-service
            port:
              number: 80
```

## Monitoring and Logging

### 1. Application Monitoring

**Prometheus Configuration**
```yaml
# prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'nova-backend'
    static_configs:
      - targets: ['nova-backend:8000']
    metrics_path: '/metrics'

  - job_name: 'nova-frontend'
    static_configs:
      - targets: ['nova-frontend:80']
```

**Grafana Dashboard**
```json
{
  "dashboard": {
    "title": "Nova Writers Dashboard",
    "panels": [
      {
        "title": "API Response Time",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(http_request_duration_seconds_sum[5m])"
          }
        ]
      },
      {
        "title": "Active Users",
        "type": "stat",
        "targets": [
          {
            "expr": "nova_active_users"
          }
        ]
      }
    ]
  }
}
```

### 2. Logging Configuration

**ELK Stack Setup**
```yaml
# docker-compose.logging.yml
version: '3.8'

services:
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.8.0
    environment:
      - discovery.type=single-node
    ports:
      - "9200:9200"
    volumes:
      - elasticsearch_data:/usr/share/elasticsearch/data

  logstash:
    image: docker.elastic.co/logstash/logstash:8.8.0
    ports:
      - "5044:5044"
    volumes:
      - ./logstash.conf:/usr/share/logstash/pipeline/logstash.conf

  kibana:
    image: docker.elastic.co/kibana/kibana:8.8.0
    ports:
      - "5601:5601"
    environment:
      - ELASTICSEARCH_HOSTS=http://elasticsearch:9200

volumes:
  elasticsearch_data:
```

## Security Considerations

### 1. SSL/TLS Configuration

```bash
# Generate SSL certificate with Let's Encrypt
sudo certbot certonly --standalone -d nova-writers.com

# Auto-renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

### 2. Firewall Configuration

```bash
# UFW firewall setup
sudo ufw allow ssh
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

### 3. Database Security

```sql
-- PostgreSQL security hardening
CREATE USER nova_user WITH PASSWORD 'secure_password';
GRANT CONNECT ON DATABASE nova_db TO nova_user;
GRANT USAGE ON SCHEMA public TO nova_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO nova_user;

-- Enable SSL
ALTER SYSTEM SET ssl = on;
ALTER SYSTEM SET ssl_cert_file = '/etc/ssl/certs/ssl-cert-snakeoil.pem';
ALTER SYSTEM SET ssl_key_file = '/etc/ssl/private/ssl-cert-snakeoil.key';
```

## Backup and Recovery

### 1. Database Backup

```bash
#!/bin/bash
# backup.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups"

# PostgreSQL backup
pg_dump $DATABASE_URL > $BACKUP_DIR/nova_db_$DATE.sql

# Redis backup
redis-cli BGSAVE
cp /var/lib/redis/dump.rdb $BACKUP_DIR/redis_$DATE.rdb

# Compress backups
tar -czf $BACKUP_DIR/nova_backup_$DATE.tar.gz $BACKUP_DIR/nova_db_$DATE.sql $BACKUP_DIR/redis_$DATE.rdb

# Upload to cloud storage
aws s3 cp $BACKUP_DIR/nova_backup_$DATE.tar.gz s3://nova-backups/

# Cleanup old backups (keep last 7 days)
find $BACKUP_DIR -name "nova_backup_*.tar.gz" -mtime +7 -delete
```

### 2. Application Backup

```bash
#!/bin/bash
# app_backup.sh

# Backup configuration files
tar -czf config_backup_$(date +%Y%m%d).tar.gz \
    .env \
    docker-compose.yml \
    nginx.conf \
    ssl/

# Backup application data
docker run --rm -v nova_postgres_data:/data -v $(pwd):/backup \
    alpine tar -czf /backup/postgres_data_$(date +%Y%m%d).tar.gz -C /data .
```

## Performance Optimization

### 1. Database Optimization

```sql
-- PostgreSQL performance tuning
ALTER SYSTEM SET shared_buffers = '256MB';
ALTER SYSTEM SET effective_cache_size = '1GB';
ALTER SYSTEM SET maintenance_work_mem = '64MB';
ALTER SYSTEM SET checkpoint_completion_target = 0.9;
ALTER SYSTEM SET wal_buffers = '16MB';
ALTER SYSTEM SET default_statistics_target = 100;

-- Create indexes for common queries
CREATE INDEX idx_memories_markers ON memories USING GIN (markers);
CREATE INDEX idx_memories_agent ON memories (agent);
CREATE INDEX idx_memories_created_at ON memories (created_at);
```

### 2. Redis Optimization

```bash
# Redis configuration optimization
maxmemory 512mb
maxmemory-policy allkeys-lru
save 900 1
save 300 10
save 60 10000
```

### 3. Application Optimization

```python
# Backend performance optimizations
# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://nova-writers.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Enable Gzip compression
app.add_middleware(GZipMiddleware, minimum_size=1000)
```

## Troubleshooting

### 1. Common Issues

**Database Connection Issues**
```bash
# Check PostgreSQL status
sudo systemctl status postgresql

# Check connection logs
sudo tail -f /var/log/postgresql/postgresql-*.log

# Test connection
psql -h localhost -U nova_user -d nova_db
```

**Redis Connection Issues**
```bash
# Check Redis status
sudo systemctl status redis

# Test Redis connection
redis-cli ping

# Check Redis logs
sudo tail -f /var/log/redis/redis-server.log
```

**Docker Issues**
```bash
# Check container status
docker ps -a

# View container logs
docker logs nova-backend

# Restart services
docker-compose restart backend
```

### 2. Performance Monitoring

```bash
# Monitor system resources
htop
iotop
nethogs

# Monitor Docker resources
docker stats

# Monitor application logs
docker-compose logs -f backend
```

---

*This deployment guide provides comprehensive instructions for deploying Nova Writers Conspiracy across various environments, from local development to production cloud deployments.* 