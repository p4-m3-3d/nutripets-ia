from fastapi import APIRouter

from app.services.faq_service import FAQService

router = APIRouter(
    prefix="/faq",
    tags=["FAQ"]
)


@router.get("/")
def get_faq():
    return FAQService.get_all_faq()