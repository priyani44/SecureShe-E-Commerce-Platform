from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Load database URL from environment variable or directly provide it here
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres-secureshe_owner:tYLwHE28IpvO@ep-wild-smoke-a1xjdvuf.ap-southeast-1.aws.neon.tech/postgres-secureshe?sslmode=require")

# Create engine
engine = create_engine(DATABASE_URL)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for our models
Base = declarative_base()

def get_session():
    # Dependency that provides a SQLAlchemy session
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Function to create all tables
def init_db():
    Base.metadata.create_all(bind=engine)
