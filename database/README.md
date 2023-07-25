# Database

## Development Environment Setup

1. Create [virtualenv](https://virtualenv.pypa.io/en/latest/user_guide.html): `virtualenv venv`
2. Install dependencies: `pip install -r requirements.txt`
3. Create new migrations according
   to [docs](https://alembic.sqlalchemy.org/en/latest/tutorial.html#create-a-migration-script):
    1. Create a revision: `alembic revision -m "create account table"`
    2. Examples:
        1. [Putting mock data into dev database](versions%2F2023_07_22_2316-0b464a1d6c9c_carbon_auditor_mock_dev_data.py)
    3. Upgrade to latest: `alembic -x env=dev upgrade head`
    4. Regenerate models - see database-gen project
