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

    return session.exec(query).first()


def find(
    *,
    session: Session,
):
    query = select(Game)
    return session.exec(query).all()


def delete(
    game_id: str,
    *,
    session: Session,
):
    game = get(game_id, session=session)

    if not game:
        return False

    session.delete(game)
    session.commit()

    return True


def create_node(
    game_id: str,
    position_id: str,
    from_san: str | None = None,
    *,
    session: Session,
):
    game = get(game_id, session=session)

    if not game:
        return None

    last_node = get_node(game, None, session=session)
    if not last_node:
        return None

    new_node = GameNode(
        game_id=game.id,
        position_id=position_id,
        from_san=from_san,
        ply=last_node.ply + 1,
    )

    session.add(new_node)
    session.commit()
    session.refresh(new_node)

    return new_node
