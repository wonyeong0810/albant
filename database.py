# database.py

from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import databases
import os
from dotenv import load_dotenv

load_dotenv()

db_token = os.getenv('DB')
# SQLAlchemy specific database URI
engine = create_engine(db_token, echo=True, future=True)


# databases package for async database connections
database = databases.Database(db_token)

# Session and Base for ORM
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
