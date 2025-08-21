from fastapi import APIRouter, status

router = APIRouter(tags=["game"])


@router.get("/", status_code=status.HTTP_501_NOT_IMPLEMENTED)
def list_games():
    pass


@router.post("/", status_code=status.HTTP_501_NOT_IMPLEMENTED)
def create_game():
    pass


@router.get("/{game_id}", status_code=status.HTTP_501_NOT_IMPLEMENTED)
def get_game(game_id: str):
    pass


@router.post("/{game_id}/moves", status_code=status.HTTP_501_NOT_IMPLEMENTED)
def make_move(game_id: str):
    pass


@router.post("/{game_id}/moves/preferred", status_code=status.HTTP_501_NOT_IMPLEMENTED)
def get_preferred_move(game_id: str, ply: int | None = None):
    pass
