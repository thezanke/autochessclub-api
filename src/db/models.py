import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Callable, List, Optional

from sqlmodel import BigInteger, Column, Field, Relationship, SQLModel, func, text

if TYPE_CHECKING:
    func: Callable


class PositionBase(SQLModel):
    fen_norm: str = Field(unique=True)
    zkey: int = Field(sa_column=Column(BigInteger, index=True))


class Position(PositionBase, table=True):
    __tablename__ = "position"

    id: uuid.UUID | None = Field(
        primary_key=True,
        sa_column_kwargs={"server_default": text("gen_random_uuid()")},
    )


class PositionPublic(PositionBase):
    id: uuid.UUID | None
    fen_norm: str
    zkey: int


class GameBase(SQLModel):
    id: uuid.UUID | None = Field(
        primary_key=True,
        sa_column_kwargs={"server_default": text("gen_random_uuid()")},
    )
    white_player_id: uuid.UUID | None = Field(index=True, nullable=True)
    black_player_id: uuid.UUID | None = Field(index=True, nullable=True)
    winner: bool | None = Field(default=None, nullable=True)
    status: str = Field(index=True, sa_column_kwargs={"server_default": "pending"})
    created_at: datetime = Field(
        default_factory=datetime.now,
        sa_column_kwargs={"server_default": func.now()},
    )


class Game(GameBase, table=True):
    __tablename__ = "game"

    nodes: Optional[List["GameNode"]] = Relationship(
        back_populates="game",
        cascade_delete=True,
        sa_relationship_kwargs={"order_by": "asc(GameNode.ply)"},
    )


class GamePublic(GameBase):
    id: uuid.UUID | None
    white_player_id: uuid.UUID | None
    black_player_id: uuid.UUID | None
    winner: bool | None
    status: str
    created_at: datetime
    nodes: List["GameNodePublic"] = []


class GameNodeBase(SQLModel):
    game_id: uuid.UUID = Field(
        foreign_key="game.id",
        primary_key=True,
        ondelete="CASCADE",
    )
    ply: int = Field(primary_key=True)
    from_san: str | None = Field(default=None, nullable=True)
    position_id: uuid.UUID = Field(
        foreign_key="position.id",
        index=True,
        ondelete="CASCADE",
    )
    white_clock: int | None = Field(default=None, nullable=True)
    black_clock: int | None = Field(default=None, nullable=True)
    created_at: datetime = Field(
        default_factory=datetime.now,
        sa_column_kwargs={"server_default": func.now()},
    )


class GameNode(GameNodeBase, table=True):
    __tablename__ = "game_node"

    game: Optional["Game"] = Relationship(back_populates="nodes")
    position: Optional["Position"] = Relationship()


class GameNodePublic(SQLModel):
    game_id: uuid.UUID
    ply: int
    position_id: uuid.UUID
    white_clock: int | None
    black_clock: int | None
    from_san: str | None
    created_at: datetime

    position: "Position" = []


class PreferredMove(SQLModel, table=True):
    __tablename__ = "preferred_move"

    player_id: uuid.UUID = Field(index=True, primary_key=True)
    position_id: uuid.UUID = Field(
        primary_key=True,
        foreign_key="position.id",
        ondelete="CASCADE",
    )
    next_position_id: uuid.UUID = Field(
        foreign_key="position.id",
        index=True,
        ondelete="CASCADE",
    )
    san: str = Field()
    created_at: datetime = Field(
        default_factory=datetime.now,
        sa_column_kwargs={"server_default": func.now()},
    )
    updated_at: datetime = Field(
        default_factory=datetime.now,
        sa_column_kwargs={
            "server_default": func.now(),
            "onupdate": func.now(),
        },
    )

    position: Optional["Position"] = Relationship(
        sa_relationship_kwargs={"foreign_keys": "[PreferredMove.position_id]"}
    )
    next_position: Optional["Position"] = Relationship(
        sa_relationship_kwargs={"foreign_keys": "[PreferredMove.next_position_id]"}
    )
