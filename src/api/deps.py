from typing import Annotated
import uuid
from fastapi.params import Depends
from sqlmodel import Session

from src.core.db import engine


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]


MOCK_PLAYER_ID = uuid.UUID("00000000-0000-0000-0000-000000000000")


def get_player_id():
    return MOCK_PLAYER_ID


PlayerIDDep = Annotated[uuid.UUID, Depends(get_player_id)]
