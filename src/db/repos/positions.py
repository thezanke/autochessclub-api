from sqlmodel import Session, select

from src.db.models import Position


def get_or_create(
    fen_norm: str,
    zkey: int,
    *,
    session: Session,
):
    position = session.exec(
        select(Position).where(Position.fen_norm == fen_norm)
    ).first()

    if position is None:
        position: Position = Position(fen_norm=fen_norm, zkey=zkey)

        session.add(position)
        session.commit()
        session.refresh(position)

    return position
