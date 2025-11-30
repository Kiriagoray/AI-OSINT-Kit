#!/bin/bash
# Create initial database migration

cd backend

echo "Creating initial database migration..."

# Check if alembic versions directory exists
if [ ! -d "alembic/versions" ]; then
    mkdir -p alembic/versions
    touch alembic/versions/__init__.py
fi

# Create migration
alembic revision --autogenerate -m "Initial migration"

echo "✅ Migration created!"
echo "Run 'alembic upgrade head' to apply it"












