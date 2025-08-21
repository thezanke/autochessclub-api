from chess import Board
from chess.polyglot import zobrist_hash

TWO64, TWO63 = 1 << 64, 1 << 63


def u64_to_i64(u: int) -> int:
    return u - TWO64 if u & TWO63 else u


def i64_to_u64(i: int) -> int:
    return i if i >= 0 else i + TWO64


def board_to_zkey(board: Board):
    return u64_to_i64(zobrist_hash(board))
