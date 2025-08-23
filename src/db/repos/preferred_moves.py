import uuid

from sqlmodel import Session

from src.db.models import PreferredMove


def get_for_position(
    player_id: uuid.UUID,
    position_id: uuid.UUID,
    *,
    session: Session,
):
    return session.get(
        PreferredMove,
        {
            "player_id": player_id,
            "position_id": position_id,
        },
    )


def create(
    player_id: uuid.UUID,
    position_id: uuid.UUID,
    next_position_id: uuid.UUID,
    san: str,
    *,
    session: Session,
):
    preferred_move = PreferredMove(
        player_id=player_id,
        position_id=position_id,
        next_position_id=next_position_id,
        san=san,
    )

    session.add(preferred_move)
    session.commit()
    session.refresh(preferred_move)

    return preferred_move
