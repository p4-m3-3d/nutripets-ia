from fastapi import APIRouter

from app.services.advice_service import AdviceService

router = APIRouter(
    prefix="/advice",
    tags=["Advice"]
)


@router.get("/")
def get_advice():
    return AdviceService.get_all_advice()