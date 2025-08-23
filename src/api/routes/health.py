from fastapi import APIRouter, status

router = APIRouter(tags=["utility"])


@router.get("/healthz", status_code=status.HTTP_204_NO_CONTENT)
def healthcheck():
    pass
