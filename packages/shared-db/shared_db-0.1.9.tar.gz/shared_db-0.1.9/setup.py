from setuptools import setup, find_packages

setup(
    name="shared-db",
    packages=find_packages(
        include=["shared_db", "shared_db.*"]
    ),  # This will include all subpackages
    version="0.1.9",
    author="AgentOS",
    description="The shared database for AgentOS",
    install_requires=[
        "sqlalchemy>=2.0.0",
        "pydantic>=2.0.0",
        "alembic>=1.14.0",
        "python-dotenv>=1.0.0",
        "psycopg2-binary>=2.9.0",
        # other dependencies
    ],
)
