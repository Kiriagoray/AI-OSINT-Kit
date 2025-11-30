# Contributing to AI OSINT Kit

Thank you for your interest in contributing to AI OSINT Kit! This document provides guidelines and instructions for contributing.

## Development Setup

1. **Fork and clone the repository**
   ```bash
   git clone <your-fork-url>
   cd AI-OSINT-Kit
   ```

2. **Set up backend**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Set up frontend**
   ```bash
   cd frontend
   npm install
   ```

4. **Set up environment**
   ```bash
   cp backend/.env.example backend/.env
   # Edit backend/.env with your configuration
   ```

5. **Start services**
   ```bash
   docker compose up postgres redis -d
   ```

6. **Run migrations**
   ```bash
   cd backend
   alembic upgrade head
   ```

## Development Workflow

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Follow the existing code style
   - Add tests for new features
   - Update documentation as needed

3. **Run tests and linting**
   ```bash
   # Backend
   cd backend
   pytest
   black --check .
   ruff check .
   
   # Frontend
   cd frontend
   npm run lint
   npm run build
   ```

4. **Commit your changes**
   ```bash
   git commit -m "feat: add your feature description"
   ```

5. **Push and create a pull request**
   ```bash
   git push origin feature/your-feature-name
   ```

## Code Style

### Backend (Python)
- Follow PEP 8
- Use Black for formatting
- Use Ruff for linting
- Type hints are encouraged
- Docstrings for all functions and classes

### Frontend (TypeScript/React)
- Use ESLint rules
- Follow React best practices
- Use TypeScript for type safety
- Prefer functional components with hooks

## Testing

- Write tests for all new features
- Maintain or improve test coverage
- Tests should be fast and isolated

## Pull Request Process

1. Update README.md with any new features or changes
2. Ensure all tests pass
3. Ensure linting passes
4. Get at least one review before merging
5. Update the roadmap if applicable

## Questions?

Open an issue for questions or discussion about the project.












