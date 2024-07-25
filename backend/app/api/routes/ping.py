from fastapi import APIRouter

from app.models import PingResponse

router = APIRouter()


@router.get("/ping", response_model=PingResponse)
def ping() -> PingResponse:
    return PingResponse(ping="pong")
