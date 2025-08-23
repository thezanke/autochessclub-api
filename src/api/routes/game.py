import chess
from fastapi import APIRouter, status, exceptions

from src.api.deps import PlayerIDDep, SessionDep
from src.db.models import GamePublic
from src.db.repos import games, positions, preferred_moves
from src.utils import board_to_zkey

router = APIRouter(
    prefix="/game",
    tags=["game"],
)


@router.get("/", response_model=list[GamePublic])
def list_games(
    *,
    session: SessionDep,
):
    return games.find(session=session)


@router.post("/", response_model=GamePublic)
def create_game(
    fen: str | None = chess.STARTING_FEN,
    *,
    session: SessionDep,
    playerId: PlayerIDDep,
):
    board = chess.Board(fen)
    starting_pos = positions.get_or_create(
        board.fen(en_passant="legal"),
        board_to_zkey(board),
        session=session,
    )
    game = games.create(starting_pos, white_player_id=playerId, session=session)

    return game


@router.get("/{game_id}", response_model=GamePublic)
def get_game(
    game_id: str,
    *,
    session: SessionDep,
):
    return games.get(game_id, session=session)


@router.post("/{game_id}/moves", response_model=GamePublic)
def make_move(
    game_id: str,
    move_san: str,
    is_preferred: bool,
    *,
    player_id: PlayerIDDep,
    session: SessionDep,
):
    game = games.get(game_id, session=session)
    if not game:
        raise exceptions.HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Game not found",
        )

    current_node = games.get_node(game, None, session=session)
    if not current_node:
        raise exceptions.HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No moves found for this game",
        )

    board = chess.Board(current_node.position.fen_norm)

    try:
        chess_move = board.parse_san(move_san)
    except ValueError as e:
        print(e)
        raise exceptions.HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid move format",
        ) from e

    if chess_move not in board.legal_moves:
        raise exceptions.HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Illegal move",
        )

    board.push(chess_move)

    new_position = positions.get_or_create(
        board.fen(en_passant="legal"),
        board_to_zkey(board),
        session=session,
    )

    new_node = games.create_node(
        game_id=game.id,
        position_id=new_position.id,
        session=session,
    )

    if is_preferred:
        preferred_moves.create(
            player_id=player_id,
            position_id=current_node.position_id,
            next_position_id=new_position.id,
            san=move_san,
            session=session,
        )

    if not new_node:
        raise exceptions.HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create new game node",
        )

    if game.status != "inprogress":
        game.status = "inprogress"

    if board.is_game_over():
        outcome = board.outcome()

        game.winner = outcome.winner
        game.status = "finished"

    session.add(game)
    session.commit()
    session.refresh(game)

    return game


@router.post("/{game_id}/moves/preferred")
def get_preferred_move(
    game_id: str,
    ply: int | None = None,
    scope: bool | None = None,
    *,
    session: SessionDep,
    playerId: PlayerIDDep,
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

    board = chess.Board(node.position.fen_norm)

    if scope is None:
        scope = board.turn
    elif scope != board.turn:
        board.turn = scope

    position = positions.get_or_create(
        board.fen(en_passant="legal"),
        board_to_zkey(board),
        session=session,
    )

    return preferred_moves.get_for_player_position(
        playerId,
        scope,
        position.id,
        session=session,
    )


@router.delete("/{game_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_game(
    game_id: str,
    *,
    session: SessionDep,
    playerId: PlayerIDDep,
):
    game = games.get(game_id, session=session)
    if not game:
        raise exceptions.HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Game not found",
        )

    if game.white_player_id != playerId:
        raise exceptions.HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this game",
        )

    games.delete(game_id, session=session)
