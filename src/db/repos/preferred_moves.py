import uuid

from sqlmodel import Session

from src.db.models import PreferredMove


def get_for_player_position(
    player_id: uuid.UUID,
    scope: str,
    position_id: uuid.UUID,
    *,
    session: Session,
):
    return session.get(
        PreferredMove,
        {
            "player_id": player_id,
            "scope": scope,
            "position_id": position_id,
        },
    )
