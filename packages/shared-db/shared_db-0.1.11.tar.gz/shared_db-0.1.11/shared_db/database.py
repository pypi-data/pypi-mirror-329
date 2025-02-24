from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import QueuePool

from contextlib import contextmanager

from .models import Base


class Database:
    def __init__(self, user: str, password: str, host: str, port: str, db_name: str):
        # Create connection URL
        self.DATABASE_URL = f"postgresql://{user}:{password}@{host}:{port}/{db_name}"

        # Create engine with connection pooling
        self.engine = create_engine(
            self.DATABASE_URL,
            poolclass=QueuePool,
            pool_size=5,  # Maximum number of connections in the pool
            max_overflow=10,  # Maximum number of connections that can be created beyond pool_size
            pool_timeout=30,  # Timeout for getting a connection from the pool
            pool_pre_ping=True,  # Enable connection health checks
        )

        # Create session factory
        self.SessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine
        )

    @contextmanager
    def get_session(self):
        """
        Get a database session. Use with a context manager:

        with db.get_session() as session:
            session.query(...)
        """
        session = self.SessionLocal()
        try:
            yield session
        finally:
            session.close()

    def create_tables(self):
        """Create all tables defined in models"""
        Base.metadata.create_all(bind=self.engine)
