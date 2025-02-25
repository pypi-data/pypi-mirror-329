from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool

from contextlib import contextmanager

from .models import Base


class Database:
    def __init__(self, url: str):
        # Create engine with connection pooling
        self.engine = create_engine(
            url,
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

    def check_connection(self):
        """Check if the connection to the database is working"""
        try:
            with self.get_session() as session:
                session.execute(text("SELECT 1"))
        except Exception as e:
            raise e
