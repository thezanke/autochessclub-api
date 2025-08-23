import uuid
import chess
from fastapi import APIRouter, status, exceptions

from src.api.deps import SessionDep
from src.db.models import GamePublic
from src.db.repos import games, positions, preferred_moves
from src.utils import board_to_zkey

router = APIRouter(
    prefix="/game",
    tags=["game"],
)

MOCK_PLAYER_ID = uuid.uuid4()


@router.get("/", status_code=status.HTTP_501_NOT_IMPLEMENTED)
def list_games():
    pass


@router.post("/", response_model=GamePublic)
def create_game(
    fen: str | None = None,
    *,
    session: SessionDep,
):
    board = chess.Board(fen)
    starting_pos = positions.get_or_create(
        board.fen(en_passant="legal"),
        board_to_zkey(board),
        session=session,
    )
    game = games.create(starting_pos, session=session)

    return game


@router.get("/{game_id}", response_model=GamePublic)
def get_game(
    game_id: str,
    *,
    session: SessionDep,
):
    return games.get(game_id, session=session)


@router.post("/{game_id}/moves", status_code=status.HTTP_501_NOT_IMPLEMENTED)
def make_move(game_id: str):
    print(f"Making move in game with ID: {game_id}")


@router.post("/{game_id}/moves/preferred")
def get_preferred_move(
    game_id: str,
    ply: int | None = None,
    scope: bool | None = None,
    *,
    session: SessionDep,
):
    node = games.get_node(
        game_id,
        ply,
        session=session,
    )

    if not node:
        raise exceptions.HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Game or node not found",
        )

    if scope is None:
        scope = chess.Board(node.position.fen_norm).turn

    return preferred_moves.get_for_player_position(
        MOCK_PLAYER_ID,
        scope,
        node.position.id,
        session=session,
    )
