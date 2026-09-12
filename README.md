# SECR TA Online Backend

## Features
- Admin account auto-created on first start
- Admin creates employee accounts
- Employees remain inactive until admin approval
- JWT login
- Employee can access only own TA entries
- Admin can view all employees and all TA entries
- SQLite works immediately for testing
- PostgreSQL supported for production

## Quick Start (Windows / Linux)
```bash
python -m venv venv
```

Windows:
```bash
venv\Scripts\activate
```

Linux/macOS:
```bash
source venv/bin/activate
```

Install:
```bash
pip install -r requirements.txt
```

Copy `.env.example` to `.env`, then change SECRET_KEY and admin password.

Run:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Open API documentation:
http://127.0.0.1:8000/docs

Default test admin comes from `.env.example`:
- HRMS ID: ADMIN001
- Password: ChangeMe123!

Change these before production.

## PostgreSQL
Set DATABASE_URL in `.env`, for example:
postgresql+psycopg://username:password@localhost:5432/secr_ta
