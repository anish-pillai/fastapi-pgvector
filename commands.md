# Create Virtual Env

python3 -m venv venv

## Activate the vitual env

source venv/bin/activate

cd fastapi-pgvector

## Start the server

uvicorn main:app --reload

## Load the swagger

[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## Initiate DB

python init_db.py

## Setup and Use Alembic

### Initial Setup

```bash
# Install required packages
python -m pip install alembic psycopg2-binary pgvector

# Initialize Alembic (creates alembic/ directory)
alembic init alembic
```

### Set Database URL

```bash
# Set for current shell
export DATABASE_URL="postgresql+psycopg2://postgres@localhost:5432/postgres"

# Or add to ~/.zshrc for persistence
echo 'export DATABASE_URL="postgresql+psycopg2://postgres@localhost:5432/postgres"' >> ~/.zshrc
source ~/.zshrc
```

### Common Alembic Commands

#### Create New Migration

```bash
# Generate migration from model changes
alembic revision --autogenerate -m "describe your changes"

# Apply migrations
alembic upgrade head
```

#### Check Migration Status

```bash
# Show current revision in DB
alembic current

# Show migration history
alembic history --verbose

# Show available heads
alembic heads
```

#### Baseline Existing DB

If your DB already has tables (e.g., created by init_db.py):

```bash
# Generate baseline migration
alembic revision --autogenerate -m "baseline"

# Mark it as applied without running SQL
alembic stamp head
```

#### Common Issues

- "Can't load plugin: sqlalchemy.dialects:driver" → Set correct DATABASE_URL
- "ModuleNotFoundError: No module named 'pgvector'" → Run `pip install pgvector`
- Database "not up to date" → Run `alembic upgrade head`
