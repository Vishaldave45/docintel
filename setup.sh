#!/bin/bash
# Quick setup script for DocIntel development environment

set -e

echo "🚀 DocIntel Development Setup Script"
echo "====================================="
echo ""

# Check prerequisites
echo "✓ Checking prerequisites..."
command -v python3 >/dev/null 2>&1 || { echo "❌ Python 3 not found"; exit 1; }
command -v node >/dev/null 2>&1 || { echo "❌ Node.js not found"; exit 1; }
command -v npm >/dev/null 2>&1 || { echo "❌ npm not found"; exit 1; }
command -v docker >/dev/null 2>&1 || { echo "❌ Docker not found"; exit 1; }

echo "✓ Python $(python3 --version | cut -d' ' -f2)"
echo "✓ Node.js $(node --version)"
echo "✓ npm $(npm --version)"
echo ""

# Backend setup
echo "📦 Setting up backend environment..."
cd backend

if [ ! -d "venv" ]; then
    echo "  Creating virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate

echo "  Upgrading pip, setuptools, wheel..."
pip install --upgrade pip setuptools wheel -q

echo "  Installing Python dependencies (this may take 5-15 minutes)..."
pip install -e . -q

echo "✓ Backend setup complete"
echo ""

# Frontend setup
echo "📦 Setting up frontend environment..."
cd ..

echo "  Installing Node.js dependencies..."
npm install -q

echo "✓ Frontend setup complete"
echo ""

# Database setup
echo "🗄️  Starting PostgreSQL container..."
if docker ps --filter "name=docintel-postgres" --format '{{.Names}}' | grep -q docintel-postgres; then
    echo "  Container already running"
else
    docker-compose up -d postgres
    echo "  Waiting for database to be ready..."
    sleep 3
fi

echo "✓ PostgreSQL is running on localhost:5432"
echo ""

# Environment configuration
echo "⚙️  Creating environment configuration..."
cd backend

if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "  ✓ Created .env from .env.example"
    echo "  ⚠️  Please review and add any API keys to .env"
else
    echo "  ✓ .env file already exists"
fi

# Database migrations
echo ""
echo "🔄 Running database migrations..."
source venv/bin/activate
alembic upgrade head

cd ..

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Add any API keys to backend/.env"
echo "2. In Terminal 1, run: cd backend && source venv/bin/activate && uvicorn app.main:app --reload"
echo "3. In Terminal 2, run: npm run dev"
echo ""
echo "Access points:"
echo "  • Backend API: http://localhost:8000"
echo "  • API Docs: http://localhost:8000/docs"
echo "  • Frontend: http://localhost:5173"
echo ""
