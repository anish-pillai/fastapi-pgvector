# FastAPI pgvector Service

A FastAPI service that uses pgvector for vector similarity search and embeddings storage.

## Quick Start

```bash
# Clone and setup
git clone git@github.com:anish-pillai/fastapi-pgvector.git
cd fastapi-pgvector

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate

# Install PDM and dependencies
pip install pdm uv
pdm install

# Start the server
pdm run start
```

The API will be available at [http://localhost:8000/docs](http://localhost:8000/docs)

## Features

- FastAPI REST API
- PostgreSQL with pgvector extension for vector similarity search
- SQLAlchemy ORM with Alembic migrations
- Modern Python dependency management with PDM

## Project Structure

```plaintext
fastapi-pgvector/
├── pyproject.toml         # Project configuration and dependencies
├── server/
│   ├── app/
│   │   ├── core/         # Core application components
│   │   │   ├── config.py       # Settings and configuration
│   │   │   ├── database.py     # Database connection
│   │   │   └── exceptions.py   # Custom exceptions
│   │   ├── models/      # Database models
│   │   │   └── models.py
│   │   ├── routes/      # API routes
│   │   │   ├── users.py
│   │   │   ├── chats.py
│   │   │   ├── messages.py
│   │   │   └── documents.py
│   │   └── schemas/     # Pydantic models
│   │       └── schemas.py
│   ├── alembic/         # Database migrations
│   ├── tests/           # Test files
│   └── main.py          # FastAPI application
└── docs/                # Additional documentation
```

## Commands

```bash
# Start the server
pdm run start  # or pdm run s

# Database Operations
pdm run migrate          # Apply migrations (alembic upgrade head)
pdm run makemigrations   # Create new migration (alembic revision --autogenerate)
pdm run db-init          # Initialize database

# Testing
pdm run test
```

See [DEVELOPER.md](DEVELOPER.md) for detailed development setup and guidelines.

## Environment Variables

- `DATABASE_URL`: PostgreSQL connection string (default: "postgresql+psycopg2://postgres@localhost:5432/postgres")

## License

[Your chosen license]