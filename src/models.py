from datetime import datetime
import uuid

from sqlmodel import BigInteger, Column, Field, SQLModel, func, text


class Position(SQLModel, table=True):
    __tablename__ = "position"

    id: uuid.UUID | None = Field(
        primary_key=True,
        sa_column_kwargs={"server_default": text("gen_random_uuid()")},
    )
    fen_norm: str = Field(unique=True)
    zkey: int = Field(sa_column=Column(BigInteger, index=True))


class PlayerMovePref(SQLModel, table=True):
    __tablename__ = "player_move_pref"

    user_id: uuid.UUID = Field(index=True, primary_key=True)
    scope: str = Field(index=True, primary_key=True)
    pos_from: uuid.UUID = Field(
        primary_key=True,
        foreign_key="position.id",
        ondelete="CASCADE",
    )
    uci: str = Field()
    pos_to: uuid.UUID = Field(foreign_key="position.id", ondelete="CASCADE")
    updated_at: datetime = Field(
        default_factory=datetime.now,
        sa_column_kwargs={
            # pylint: disable=not-callable
            "server_default": func.now(),
            "onupdate": func.now(),
            # pylint: enable=not-callable
        },
    )
