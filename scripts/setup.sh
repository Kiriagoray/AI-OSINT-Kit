#!/bin/bash
# Setup script for AI OSINT Kit

set -e

echo "🚀 Setting up AI OSINT Kit..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker and try again."
    exit 1
fi

# Copy environment file if it doesn't exist
if [ ! -f backend/.env ]; then
    echo "📝 Creating backend/.env from .env.example..."
    cp backend/.env.example backend/.env
    echo "⚠️  Please edit backend/.env with your API keys and configuration"
fi

# Start services
echo "🐳 Starting Docker services..."
docker compose up -d postgres redis

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 5

# Run migrations
echo "🗄️  Running database migrations..."
docker compose exec backend alembic upgrade head || echo "⚠️  Migrations will run on first backend start"

# Install Python dependencies (if running locally)
if [ -d "backend/venv" ]; then
    echo "📦 Installing Python dependencies..."
    source backend/venv/bin/activate
    pip install -r backend/requirements.txt
fi

# Install Node dependencies (if running locally)
if [ -d "frontend/node_modules" ]; then
    echo "📦 Node modules already installed"
else
    echo "📦 Installing Node dependencies..."
    cd frontend && npm install && cd ..
fi

echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit backend/.env with your API keys"
echo "2. Start all services: docker compose up"
echo "3. Access frontend at http://localhost:3000"
echo "4. Access backend API at http://localhost:8000"
echo "5. Pull Ollama model: docker exec osintkit-ollama ollama pull llama3"












