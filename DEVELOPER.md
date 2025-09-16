# Developer Guide

## Development Setup

### Prerequisites

- Python 3.11+
- PostgreSQL with pgvector extension
- PDM (Python dependency manager)

### First-Time Setup

1. **Clone and Create Virtual Environment**:

   ```bash
   # Clone the repository
   git clone git@github.com:yourusername/fastapi-pgvector.git
   cd fastapi-pgvector

   # Create virtual environment
   python3 -m venv venv

   # Activate virtual environment
   # On macOS/Linux:
   source venv/bin/activate
   # On Windows:
   # .\venv\Scripts\activate

   # Verify python is from venv
   which python  # Should show path to venv/bin/python
   ```

2. **Install Dependencies**:

   ```bash
   # Install PDM (inside virtual environment)
   pip install pdm uv

   # Install project dependencies (uses uv for speed)
   pdm install
   ```

3. **Virtual Environment Tips**:

   ```bash
   # To activate the environment (add to ~/.zshrc for convenience)
   alias venv='source venv/bin/activate'

   # To deactivate when you're done
   deactivate

   # To delete and recreate if things get messy
   deactivate  # if active
   rm -rf venv
   python3 -m venv venv
   source venv/bin/activate
   pip install pdm uv
   pdm install
   ```

2. **Database Setup**:
   ```bash
   # Start PostgreSQL (if not running)
   brew services start postgresql

   # Create database and enable pgvector
   psql postgres
   CREATE EXTENSION IF NOT EXISTS vector;
   \q

   # Initialize database and apply migrations
   pdm run db-init
   pdm run migrate
   ```

## Development Workflow

### Common Commands

```bash
# Start development server (with auto-reload)
pdm run start     # or shorter: pdm run s

# Database migrations
pdm run makemigrations  # or shorter: pdm run mm
pdm run migrate        # or shorter: pdm run m

# Run tests
pdm run test
```

### Working with Migrations

1. **Create a new migration**:
   ```bash
   pdm run makemigrations
   ```

2. **Review the generated migration** in `server/alembic/versions/`

3. **Apply migrations**:
   ```bash
   pdm run migrate
   ```

4. **Check migration status**:
   ```bash
   cd server && alembic current
   cd server && alembic history --verbose
   ```

### Best Practices

1. **Database Changes**:
   - Always use migrations for schema changes
   - Review migration files before applying
   - Consider data migration needs
   - Test migrations on a copy of production data

2. **Code Organization**:
   - Keep models in `db.py`
   - API routes in `main.py`
   - Pydantic schemas in `schemas.py`
   - Complex business logic in separate modules

3. **Environment Variables**:
   ```bash
   # Required for database connection
   export DATABASE_URL="postgresql+psycopg2://postgres@localhost:5432/postgres"
   ```

## Troubleshooting

### Common Issues

1. **"Can't load plugin: sqlalchemy.dialects:driver"**
   - Ensure DATABASE_URL is set correctly
   - Check if psycopg2-binary is installed

2. **"ModuleNotFoundError: No module named 'pgvector'"**
   - Run: `pdm install` to install all dependencies
   - Verify pgvector extension is enabled in PostgreSQL

3. **"Database is not up to date"**
   - Run: `pdm run migrate`
   - Check: `cd server && alembic current`

### Maintenance Tasks

1. **Update Dependencies**:
   ```bash
   pdm update
   ```

2. **Clean Python Cache**:
   ```bash
   find . -type d -name "__pycache__" -exec rm -r {} +
   ```

3. **Reset Database** (development only):
   ```bash
   dropdb postgres && createdb postgres
   psql postgres -c 'CREATE EXTENSION vector;'
   pdm run db-init
   pdm run migrate
   ```

## API Documentation

- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## Project Structure

```plaintext
fastapi-pgvector/
├── pyproject.toml         # Project configuration and dependencies
├── README.md             # User-facing documentation
├── DEVELOPER.md          # This file - development guide
└── server/
    ├── app/              # Application package
    │   ├── core/         # Core application components
    │   │   ├── config.py       # Settings and configuration
    │   │   ├── database.py     # Database connection
    │   │   └── exceptions.py   # Custom exceptions
    │   ├── models/            # Database models
    │   │   └── models.py      # SQLAlchemy models
    │   ├── routes/            # API routes
    │   │   ├── users.py       # User endpoints
    │   │   ├── chats.py       # Chat endpoints
    │   │   ├── messages.py    # Message endpoints
    │   │   └── documents.py   # Document endpoints
    │   └── schemas/           # Data models
    │       └── schemas.py     # Pydantic models
    ├── alembic/          # Database migrations
    │   ├── versions/     # Migration files
    │   └── env.py        # Alembic configuration
    ├── tests/            # Test files
    └── main.py           # FastAPI application entry point
```

## Git Workflow

1. **Feature Development**:
   ```bash
   git checkout -b feature/your-feature
   # Make changes
   git add .
   git commit -m "feat: your feature description"
   git push origin feature/your-feature
   ```

2. **Database Changes**:
   ```bash
   # Create branch
   git checkout -b feature/db-change
   
   # Make model changes in db.py
   pdm run makemigrations
   
   # Review migration file
   pdm run migrate
   
   # Commit both model and migration
   git add server/db.py server/alembic/versions/
   git commit -m "feat(db): describe your changes"
   ```

## Adding New Dependencies

```bash
# Add production dependency
pdm add package-name

# Add development dependency
pdm add -d package-name
```

## Running in Production

1. **Environment Setup**:
   ```bash
   cd server
   cp .env.example .env
   ```

2. **Start Server**:
   ```bash
   # Using uvicorn directly
   uvicorn server.main:app --host 0.0.0.0 --port 8000
   
   # Or using PDM script
   pdm run start
   ```

## Getting Help

1. Check this guide first
2. Review [FastAPI documentation](https://fastapi.tiangolo.com/)
3. Search [SQLAlchemy docs](https://docs.sqlalchemy.org/)
4. Consult [Alembic documentation](https://alembic.sqlalchemy.org/)