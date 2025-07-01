#!/bin/bash

# 🌌 NOVA: The Writers' Conspiracy - Setup Script
# A ritual to awaken the cosmic atelier where storytellers conspire with AI

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# ASCII Art Banner
echo -e "${PURPLE}"
cat << "EOF"
🌌 NOVA: The Writers' Conspiracy 🌌
*"They said creation was lonely. They were wrong."*

A cosmic atelier where storytellers conspire with AI
EOF
echo -e "${NC}"

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   print_error "This script should not be run as root"
   exit 1
fi

# Check if Docker is installed
check_docker() {
    print_status "Checking Docker installation..."
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed. Please install Docker first."
        print_status "Visit: https://docs.docker.com/get-docker/"
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose is not installed. Please install Docker Compose first."
        print_status "Visit: https://docs.docker.com/compose/install/"
        exit 1
    fi
    
    print_success "Docker and Docker Compose are installed"
}

# Check if Node.js is installed
check_nodejs() {
    print_status "Checking Node.js installation..."
    if ! command -v node &> /dev/null; then
        print_error "Node.js is not installed. Please install Node.js 18+ first."
        print_status "Visit: https://nodejs.org/"
        exit 1
    fi
    
    NODE_VERSION=$(node --version | cut -d'v' -f2 | cut -d'.' -f1)
    if [ "$NODE_VERSION" -lt 18 ]; then
        print_error "Node.js version 18+ is required. Current version: $(node --version)"
        exit 1
    fi
    
    print_success "Node.js $(node --version) is installed"
}

# Check if Python is installed
check_python() {
    print_status "Checking Python installation..."
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3.11+ is not installed. Please install Python first."
        print_status "Visit: https://www.python.org/downloads/"
        exit 1
    fi
    
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
    PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d'.' -f1)
    PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d'.' -f2)
    
    if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 11 ]); then
        print_error "Python 3.11+ is required. Current version: $PYTHON_VERSION"
        exit 1
    fi
    
    print_success "Python $PYTHON_VERSION is installed"
}

# Create environment file
setup_environment() {
    print_status "Setting up environment configuration..."
    
    if [ ! -f .env ]; then
        if [ -f .env.example ]; then
            cp .env.example .env
            print_success "Created .env file from .env.example"
            print_warning "Please edit .env file with your API keys and configuration"
        else
            print_error ".env.example file not found"
            exit 1
        fi
    else
        print_warning ".env file already exists. Skipping creation."
    fi
}

# Install backend dependencies
setup_backend() {
    print_status "Setting up NOVA backend..."
    
    if [ ! -d "backend" ]; then
        print_error "Backend directory not found"
        exit 1
    fi
    
    cd backend
    
    # Create virtual environment if it doesn't exist
    if [ ! -d "venv" ]; then
        print_status "Creating Python virtual environment..."
        python3 -m venv venv
        print_success "Virtual environment created"
    fi
    
    # Activate virtual environment
    print_status "Activating virtual environment..."
    source venv/bin/activate
    
    # Upgrade pip
    print_status "Upgrading pip..."
    pip install --upgrade pip
    
    # Install dependencies
    if [ -f "requirements.txt" ]; then
        print_status "Installing Python dependencies..."
        pip install -r requirements.txt
        print_success "Backend dependencies installed"
    else
        print_warning "requirements.txt not found. Skipping dependency installation."
    fi
    
    cd ..
}

# Install frontend dependencies
setup_frontend() {
    print_status "Setting up NOVA frontend..."
    
    if [ ! -d "frontend" ]; then
        print_error "Frontend directory not found"
        exit 1
    fi
    
    cd frontend
    
    # Install Node.js dependencies
    if [ -f "package.json" ]; then
        print_status "Installing Node.js dependencies..."
        npm install
        print_success "Frontend dependencies installed"
    else
        print_warning "package.json not found. Skipping dependency installation."
    fi
    
    cd ..
}

# Start Docker services
start_services() {
    print_status "Starting NOVA services with Docker Compose..."
    
    # Check if Docker daemon is running
    if ! docker info &> /dev/null; then
        print_error "Docker daemon is not running. Please start Docker first."
        exit 1
    fi
    
    # Start services
    docker-compose up -d
    
    print_success "NOVA services started successfully"
    print_status "Services are starting up. This may take a few minutes..."
    
    # Wait for services to be ready
    print_status "Waiting for services to be ready..."
    sleep 30
    
    # Check service status
    print_status "Checking service status..."
    docker-compose ps
}

# Run database migrations
run_migrations() {
    print_status "Running database migrations..."
    
    cd backend
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Check if alembic is available
    if command -v alembic &> /dev/null; then
        alembic upgrade head
        print_success "Database migrations completed"
    else
        print_warning "Alembic not found. Skipping migrations."
    fi
    
    cd ..
}

# Create initial data
create_initial_data() {
    print_status "Creating initial data..."
    
    cd backend
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Run initial data creation script if it exists
    if [ -f "scripts/create_initial_data.py" ]; then
        python scripts/create_initial_data.py
        print_success "Initial data created"
    else
        print_warning "Initial data script not found. Skipping."
    fi
    
    cd ..
}

# Display final information
display_info() {
    echo -e "${CYAN}"
    echo "🌌 NOVA: The Writers' Conspiracy - Setup Complete! 🌌"
    echo ""
    echo "Your cosmic atelier is ready. Here's what you need to know:"
    echo ""
    echo "📱 Frontend: http://localhost:3000"
    echo "🔧 Backend API: http://localhost:8000"
    echo "📚 API Documentation: http://localhost:8000/docs"
    echo ""
    echo "🐳 Docker Services:"
    echo "  - nova-frontend: React development server"
    echo "  - nova-backend: FastAPI backend"
    echo "  - nova-postgres: PostgreSQL database"
    echo "  - nova-redis: Redis cache and task queue"
    echo "  - nova-celery-worker: Background task processing"
    echo "  - nova-celery-beat: Scheduled task processing"
    echo ""
    echo "📝 Next Steps:"
    echo "1. Edit .env file with your API keys"
    echo "2. Visit http://localhost:3000 to access NOVA"
    echo "3. Create your first project and start conspiring!"
    echo ""
    echo "🛠️ Useful Commands:"
    echo "  - View logs: docker-compose logs -f"
    echo "  - Stop services: docker-compose down"
    echo "  - Restart services: docker-compose restart"
    echo "  - Update services: docker-compose pull && docker-compose up -d"
    echo ""
    echo "🌌 Welcome to the conspiracy, storyteller! 🌌"
    echo -e "${NC}"
}

# Main setup function
main() {
    print_status "Beginning NOVA setup ritual..."
    
    # Check prerequisites
    check_docker
    check_nodejs
    check_python
    
    # Setup environment
    setup_environment
    
    # Setup backend
    setup_backend
    
    # Setup frontend
    setup_frontend
    
    # Start services
    start_services
    
    # Run migrations
    run_migrations
    
    # Create initial data
    create_initial_data
    
    # Display final information
    display_info
}

# Run main function
main "$@" 