from sqlmodel import Session, select

from src.db.models import Position


def get_one(fen_norm: str, zkey: int, *, session: Session):
    return session.exec(
        select(Position).where(Position.zkey == zkey, Position.fen_norm == fen_norm)
    ).first()


def get_or_create_one(
    fen_norm: str,
    zkey: int,
    *,
    session: Session,
):
    position = get_one(fen_norm, zkey, session=session)

    if position is None:
        position: Position = Position(fen_norm=fen_norm, zkey=zkey)

        session.add(position)
        session.commit()
        session.refresh(position)

    return position


def get_by_id(
    position_id: int,
    *,
    session: Session,
):
    return session.get(Position, position_id)
