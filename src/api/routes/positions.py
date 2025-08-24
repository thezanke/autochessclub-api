import chess
from fastapi import APIRouter, exceptions
from pydantic import BaseModel

from src.api.deps import PlayerIDDep, SessionDep
from src.db.models import Position, PositionPublic, PreferredMove
from src.db.repos import positions, preferred_moves
from src.utils import board_to_zkey

router = APIRouter(
    prefix="/positions",
    tags=["positions"],
)


class PositionResponse(BaseModel):
    position: PositionPublic
    preferred_move: PreferredMove | None = None


@router.get("/")
def get_position(
    position_id: str | None = None,
    fen: str | None = None,
    *,
    session: SessionDep,
    player_id: PlayerIDDep
):
    position: Position | None = None

    if position_id is not None:
        try:
            position = positions.get_by_id(position_id=position_id, session=session)
        except Exception as e:
            raise exceptions.HTTPException(
                status_code=404,
                detail="Position not found",
            ) from e

    if position is None:
        if fen is None:
            raise exceptions.HTTPException(
                status_code=400,
                detail="Either position_id or fen must be provided",
            )
        board = chess.Board(fen)
        position = positions.get_or_create(
            fen_norm=board.fen(en_passant="legal"),
            zkey=board_to_zkey(board),
            session=session,
        )

    preferred_move = preferred_moves.get_for_position(
        player_id=player_id,
        position_id=position.id,
        session=session,
    )

    return PositionResponse(
        position=position,
        preferred_move=preferred_move,
    )
