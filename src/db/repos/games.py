from sqlmodel import Session, desc, select

from src.db.models import Game, GameNode, Position


def create(
    starting_pos: Position,
    white_player_id: str | None = None,
    black_player_id: str | None = None,
    *,
    session: Session,
):
    game = Game(
        white_player_id=white_player_id,
        black_player_id=black_player_id,
        nodes=[
            GameNode(
                position_id=starting_pos.id,
                ply=1,
            )
        ],
    )

    session.add(game)
    session.commit()
    session.refresh(game)

    return game


def get(
    game_id: str,
    *,
    session: Session,
):
    return session.get(Game, game_id)


def get_node(
    game: str | Game,
    ply: int,
    *,
    session: Session,
):
    if isinstance(game, str):
        game = get(game, session=session)

    query = select(GameNode).order_by(desc(GameNode.ply)).where(GameNode.game == game)

    if ply is not None:
        query = query.where(GameNode.ply == ply)

    return session.exec(query).one_or_none()
