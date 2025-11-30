# AI-Powered OSINT Kit

A comprehensive, production-grade AI-powered Open Source Intelligence (OSINT) toolkit with a React dashboard frontend and Python FastAPI backend. Built to support local LLMs (Llama 3 / Mistral) with optional OpenAI API fallback.

## Features

- **Multi-source OSINT Collection**: WHOIS, SSL certificates, passive DNS, Shodan, HaveIBeenPwned, social handle discovery, and more
- **AI-Powered Analysis**: Local LLM integration (Ollama) with OpenAI fallback for intelligent summarization and risk assessment
- **Interactive Dashboard**: React-based UI with search, entity pages, network graphs, and real-time scan updates
- **Background Processing**: Celery-based task queue for async OSINT scans
- **Relationship Graphs**: Visualize connections between entities using Cytoscape.js
- **Structured Storage**: PostgreSQL database with support for embeddings (PGVector)

## Architecture

```
User (Browser/React)
  ↕ HTTPS REST/WebSocket
API Gateway / FastAPI (Python)
  ↕
Postgres (primary DB)  ← Celery/Redis → Background workers
  ↕
Vector store (PGVector) / Optional: Milvus
Local LLM runtime (Ollama)
OSINT integrations (Shodan, HIBP, WHOIS, SSL, etc.)
```

## Tech Stack

### Backend
- Python 3.11+ with FastAPI
- PostgreSQL with SQLAlchemy (async)
- Celery + Redis for background tasks
- Alembic for database migrations
- Ollama for local LLM inference
- OpenAI API (optional fallback)

### Frontend
- React 18 with TypeScript
- Vite for build tooling
- Tailwind CSS for styling
- React Router for navigation
- Cytoscape.js for network graphs
- Recharts for data visualization

## Quick Start

### Prerequisites

- Docker and Docker Compose
- Python 3.11+ (for local development)
- Node.js 20+ (for local frontend development)

### Using Docker Compose (Recommended)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd AI-OSINT-Kit
   ```

2. **Set up environment variables**
   ```bash
   cp backend/.env.example backend/.env
   # Edit backend/.env with your API keys and configuration
   ```

3. **Start services**
   ```bash
   docker compose up --build
   ```

4. **Initialize database**
   ```bash
   docker compose exec backend alembic upgrade head
   ```

5. **Pull Ollama model (optional)**
   ```bash
   docker exec osintkit-ollama ollama pull llama3
   ```

6. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

### Local Development

#### Backend

1. **Set up Python environment**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Set up database**
   ```bash
   # Start PostgreSQL and Redis (using Docker Compose or local install)
   docker compose up postgres redis -d
   
   # Run migrations
   alembic upgrade head
   ```

3. **Run development server**
   ```bash
   uvicorn main:app --reload
   ```

#### Frontend

1. **Install dependencies**
   ```bash
   cd frontend
   npm install
   ```

2. **Run development server**
   ```bash
   npm run dev
   ```

3. **Access at** http://localhost:5173

## Project Structure

```
AI-OSINT-Kit/
├── backend/
│   ├── app/
│   │   ├── api/           # API routes and endpoints
│   │   ├── core/          # Configuration and settings
│   │   ├── db/            # Database connection and session
│   │   ├── models/        # SQLAlchemy models
│   │   ├── services/      # Business logic (LLM, OSINT modules)
│   │   └── tasks/         # Celery background tasks
│   ├── alembic/           # Database migrations
│   ├── main.py            # FastAPI application entry point
│   └── requirements.txt   # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── pages/         # Page components
│   │   ├── App.tsx        # Main app component
│   │   └── main.tsx       # Entry point
│   └── package.json       # Node dependencies
├── infra/                 # Infrastructure configs
├── docker-compose.yml     # Docker Compose configuration
└── README.md             # This file
```

## API Endpoints

### Core Endpoints

- `GET /health` - Health check endpoint
- `GET /api/v1/scan` - List all scans
- `POST /api/v1/scan` - Start a new OSINT scan
- `GET /api/v1/scan/{id}` - Get scan status and summary with entities and findings
- `GET /api/v1/entity/{id}` - Get entity details with findings
- `GET /api/v1/entity/{id}/findings` - Get all findings for an entity
- `GET /api/v1/search?q=...` - Search entities and scans
- `GET /api/v1/report/{id}` - Get generated LLM report
- `GET /api/v1/report/scan/{scan_id}` - Get all reports for a scan
- `POST /api/v1/report/{scan_id}/generate` - Generate report from scan data (LLM integration pending)
- `WebSocket /ws/scans/{scan_id}` - Real-time scan progress updates (pending)

See `/docs` for interactive API documentation.

## Configuration

### Environment Variables

Key configuration options in `backend/.env`:

- `DATABASE_URL` - PostgreSQL connection string
- `REDIS_URL` - Redis connection string
- `LLM_BACKEND` - LLM backend (`ollama` or `openai`)
- `OLLAMA_BASE_URL` - Ollama server URL
- `OPENAI_API_KEY` - OpenAI API key (if using OpenAI)
- `SHODAN_API_KEY` - Shodan API key
- `HIBP_API_KEY` - HaveIBeenPwned API key

See `backend/.env.example` for all available options.

## Development Roadmap

### Phase 1 - MVP Backend & Core OSINT (✅ Complete)
- [x] Database models and migrations
- [x] Basic API endpoints (scan, entity, search, report)
- [x] WHOIS module
- [x] SSL certificate module
- [x] Celery task integration
- [x] Database persistence for entities and findings

### Phase 2 - LLM Integration & Reports (🚧 In Progress)
- [x] Report API endpoints
- [ ] Ollama integration for report generation
- [ ] Embedding pipeline
- [ ] Report generation with LLM
- [ ] RAG implementation

### Phase 3 - Frontend & UX (✅ Complete)
- [x] Basic UI structure
- [x] Dashboard with scan listing
- [x] Scan creation page
- [x] Scan detail page with entities and findings
- [x] Entity detail pages
- [x] Network graph visualization (Cytoscape.js)
- [x] Reports page
- [ ] WebSocket integration for real-time updates

### Phase 4 - Advanced Features
- [ ] Additional OSINT modules (Shodan, HIBP, etc.)
- [ ] Scheduled recurring scans
- [ ] User authentication and authorization
- [ ] Audit logs
- [ ] Export functionality (CSV, JSON, PDF)

### Phase 5 - Deployment & Hardening
- [ ] Production Docker configuration
- [ ] Secrets management
- [ ] Monitoring and logging
- [ ] Load testing

## Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

## Contributing

1. Create a feature branch
2. Make your changes
3. Add tests
4. Run linting and tests
5. Submit a pull request

## Security & Legal Notes

- ⚠️ **Respect Terms of Service**: Ensure compliance with all API and service terms
- ⚠️ **Data Privacy**: Comply with GDPR and local data protection laws
- ⚠️ **Rate Limiting**: Implement delays to avoid IP blocking
- ⚠️ **API Keys**: Never commit API keys to version control

## License

[Specify your license here]

## Support

For issues and questions, please open an issue on GitHub.












