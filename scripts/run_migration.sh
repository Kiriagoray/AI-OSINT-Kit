#!/bin/bash
# Run database migration

set -e

echo "🗄️  Running database migration..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker and try again."
    exit 1
fi

# Check if backend container is running
if ! docker compose ps | grep -q "osintkit-backend.*Up"; then
    echo "⚠️  Backend container is not running. Starting it..."
    docker compose up -d backend
    echo "⏳ Waiting for backend to be ready..."
    sleep 3
fi

# Run migration
echo "Running Alembic migration..."
docker compose exec backend alembic upgrade head

echo "✅ Migration completed successfully!"

# Verify tables were created
echo ""
echo "📊 Verifying database tables..."
docker compose exec -T postgres psql -U postgres -d osintkit -c "\dt"

echo ""
echo "✅ Migration verification complete!"











