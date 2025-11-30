# Quick Setup Guide

This guide will help you get the AI OSINT Kit up and running quickly.

## Prerequisites

- Docker and Docker Compose installed
- Git installed
- (Optional) Python 3.11+ and Node.js 20+ for local development

## Quick Start (5 minutes)

### 1. Clone and Setup

```bash
# Clone the repository
git clone <repository-url>
cd AI-OSINT-Kit

# Copy environment file
cp backend/.env.example backend/.env
```

### 2. Start Services

```bash
# Start all services (PostgreSQL, Redis, Backend, Frontend, Ollama)
docker compose up --build
```

This will:
- Start PostgreSQL database
- Start Redis for Celery
- Build and start FastAPI backend
- Build and start React frontend
- Start Ollama for local LLM

### 3. Initialize Database

In a new terminal:

```bash
# Run migrations
docker compose exec backend alembic upgrade head

# Or create initial migration if needed
docker compose exec backend alembic revision --autogenerate -m "Initial migration"
docker compose exec backend alembic upgrade head
```

### 4. (Optional) Pull Ollama Model

```bash
# Pull a model for local LLM inference
docker exec osintkit-ollama ollama pull llama3

# Or use a smaller model
docker exec osintkit-ollama ollama pull mistral
```

### 5. Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Ollama**: http://localhost:11434

## Configuration

### Essential Settings

Edit `backend/.env`:

```env
# Database (defaults work with Docker Compose)
DATABASE_URL=postgresql+asyncpg://postgres:postgres@postgres:5432/osintkit

# LLM Backend
LLM_BACKEND=ollama  # or 'openai'
OLLAMA_BASE_URL=http://ollama:11434

# API Keys (optional for MVP)
SHODAN_API_KEY=your_key_here
HIBP_API_KEY=your_key_here
```

### API Keys

The following API keys are optional but enable additional OSINT modules:

- **Shodan**: For IP and port scanning
- **HaveIBeenPwned**: For breach checking
- **Hunter.io**: For email discovery

You can start without these and add them later.

## Development Mode

### Backend Development

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Start services (PostgreSQL, Redis)
docker compose up postgres redis -d

# Run backend locally
uvicorn main:app --reload
```

### Frontend Development

```bash
cd frontend
npm install

# Start dev server
npm run dev
```

Frontend will run on http://localhost:5173 with hot reload.

## Testing

### Backend Tests

```bash
cd backend
pytest
```

### Frontend Tests

```bash
cd frontend
npm test  # When tests are added
```

## Troubleshooting

### Database Connection Issues

```bash
# Check if PostgreSQL is running
docker compose ps postgres

# Check logs
docker compose logs postgres
```

### Backend Not Starting

```bash
# Check backend logs
docker compose logs backend

# Ensure dependencies are installed
docker compose exec backend pip list
```

### Frontend Build Issues

```bash
# Clear node_modules and reinstall
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### Ollama Model Not Loading

```bash
# Check Ollama status
docker exec osintkit-ollama ollama list

# Pull model if missing
docker exec osintkit-ollama ollama pull llama3
```

## Next Steps

1. **Create your first scan**: Visit http://localhost:3000 and click "New Scan"
2. **Explore the API**: Visit http://localhost:8000/docs
3. **Read the documentation**: See README.md for detailed information
4. **Check project status**: See PROJECT_STATUS.md for current phase

## Getting Help

- Check the [README.md](./README.md) for detailed documentation
- Review [PROJECT_STATUS.md](./PROJECT_STATUS.md) for current development status
- Open an issue on GitHub for bugs or questions












