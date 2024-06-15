from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from src.infrastructure.configs.enviroment import get_environment_variables

# Runtime Environment Configuration
env = get_environment_variables()

# Generate Database URL
DATABASE_URL = f"{env.DATABASE_DIALECT}://{env.DATABASE_USERNAME}:{env.DATABASE_PASSWORD}@{env.DATABASE_HOSTNAME}:{env.DATABASE_PORT}/{env.DATABASE_NAME}"

# Create Database Engine
engine = create_engine(
    DATABASE_URL, echo=env.DEBUG_MODE, future=True
)

session_local = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)


def get_db_connection():
    db = scoped_session(session_local)
    
    try:
        yield db
    finally:
        db.close()
