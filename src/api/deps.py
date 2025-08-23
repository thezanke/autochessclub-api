from typing import Annotated
from fastapi.params import Depends
from sqlmodel import Session

from src.core.db import engine


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
