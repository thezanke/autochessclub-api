from sqlmodel import create_engine

from src.core.config import settings

engine = create_engine(str(settings.DATABASE_URI))
