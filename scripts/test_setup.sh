#!/bin/bash
# Test script for AI-OSINT-Kit setup and migration

set -e

echo "🧪 Testing AI-OSINT-Kit Setup..."
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker and try again."
    exit 1
fi

# Check if services are running
echo "📋 Checking Docker services..."
if ! docker compose ps | grep -q "osintkit-postgres.*Up"; then
    echo "⚠️  PostgreSQL is not running. Starting services..."
    docker compose up -d postgres redis
    echo "⏳ Waiting for services to be ready..."
    sleep 5
else
    echo "✅ PostgreSQL is running"
fi

# Run migration
echo ""
echo "🗄️  Running database migration..."
docker compose exec -T backend alembic upgrade head || {
    echo "⚠️  Migration failed. Trying alternative approach..."
    # If backend container isn't running, we need to run migration differently
    echo "Please ensure backend container is running: docker compose up -d backend"
    exit 1
}

echo "✅ Migration completed successfully!"
echo ""

# Test database connection
echo "🔍 Testing database connection..."
docker compose exec -T postgres psql -U postgres -d osintkit -c "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public';" || {
    echo "⚠️  Could not connect to database"
    exit 1
}

echo "✅ Database connection successful!"
echo ""

# List created tables
echo "📊 Database tables:"
docker compose exec -T postgres psql -U postgres -d osintkit -c "\dt" || true

echo ""
echo "✅ Setup test completed successfully!"
echo ""
echo "Next steps:"
echo "1. Start all services: docker compose up"
echo "2. Test the API: curl http://localhost:8000/health"
echo "3. Create a scan: curl -X POST http://localhost:8000/api/v1/scan -H 'Content-Type: application/json' -d '{\"target\":\"example.com\",\"type\":\"domain\",\"modules\":[\"whois\",\"ssl\"]}'"











