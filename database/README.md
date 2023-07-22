# Database
## Development Environment Setup
1. Create [virtualenv](https://virtualenv.pypa.io/en/latest/user_guide.html): `virtualenv venv`
2. Install dependencies: `pip install -r requirements.txt`
3. Create new migrations according to [docs](https://alembic.sqlalchemy.org/en/latest/tutorial.html#create-a-migration-script):
   1. Create a revision: `alembic revision -m "create account table"`
   2. Upgrade to latest: `alembic upgrade head`
