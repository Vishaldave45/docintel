# DocIntel Quick Start (5-Minute Setup)

A streamlined guide to get DocIntel running locally in minutes.

## Prerequisites Check

```bash
python3 --version  # >= 3.11
node --version     # >= 20
npm --version      # >= 10
docker --version   # installed
```

## Quick Setup Steps

### 1. Backend Setup (5-10 min)

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip setuptools wheel

# Install dependencies (large, may take 5-15 minutes due to PyTorch)
pip install -e .
```

**Note**: The first install downloads PyTorch and ML models (~2GB). Subsequent installs are instant.

### 2. Frontend Setup (30 seconds)

```bash
cd ..
npm install
```

### 3. Database Setup (1 minute)

```bash
# Start PostgreSQL
docker-compose up -d

# Verify it's running
docker-compose ps
```

### 4. Environment Configuration (30 seconds)

Create `backend/.env`:

```bash
cd backend
cat > .env << 'EOF'
ENV=development
DEBUG=true
DATABASE_URL=postgresql+asyncpg://docintel:docintel_secret_password@localhost:5432/docintel_db
LOG_LEVEL=INFO
EOF
```

### 5. Database Migrations (30 seconds)

```bash
source venv/bin/activate
alembic upgrade head
```

### 6. Run Development Servers

**Terminal 1 — Backend**:
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload
```

**Terminal 2 — Frontend**:
```bash
npm run dev
```

✅ **Done!** Access:
- Backend API: `http://localhost:8000`
- API Docs: `http://localhost:8000/docs`
- Frontend: `http://localhost:5173`

---

## Key Commands

| Task | Command |
|------|---------|
| Start database | `docker-compose up -d` |
| Stop database | `docker-compose down` |
| Run backend | `cd backend && source venv/bin/activate && uvicorn app.main:app --reload` |
| Run frontend | `npm run dev` |
| Run tests | `cd backend && pytest tests/` |
| Type check | `npm run lint` |
| Build frontend | `npm run build` |

---

## Troubleshooting

**Backend module errors?**
```bash
cd backend
source venv/bin/activate
python -c "import app"
```

**Database connection refused?**
```bash
docker-compose down && docker-compose up -d
docker-compose logs postgres
```

**Frontend won't build?**
```bash
rm -rf node_modules package-lock.json
npm install
```

**PyTorch download timeout?**
```bash
pip install --default-timeout=1000 -e .
```

---

For detailed setup, see [DEVELOPMENT.md](DEVELOPMENT.md).
