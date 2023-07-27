# Database migration scripts

To create a new [migration](https://alembic.sqlalchemy.org/en/latest/tutorial.html#create-a-migration-script):

1. Create a revision: `alembic revision -m "create account table"`
2. Examples:
    1. [Putting mock data into dev database](versions%2F2023_07_22_2316-0b464a1d6c9c_carbon_auditor_mock_dev_data.py)
3. Upgrade to latest:
    1. Dev DB: `export APP_ENV=dev && alembic upgrade head`
    2. Prod DB: `export APP_ENV=prod && alembic upgrade head`
4. Regenerate models - see database-gen project
