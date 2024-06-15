from sqlalchemy.ext.declarative import declarative_base

from src.infrastructure.configs.database import engine

# Base Entity Model Schema
entity_meta = declarative_base()


def init():
    entity_meta.metadata.create_all(bind=engine)
