from fastapi import APIRouter

from app.services.data_loader import DataLoader

router = APIRouter(
    prefix="/loader",
    tags=["Data Loader"]
)


@router.post("/recipes")
def load_recipes():
    return DataLoader.load_recipes()


@router.post("/advice")
def load_advice():
    return DataLoader.load_advice()


@router.post("/faq")
def load_faq():
    return DataLoader.load_faq()


@router.post("/toxic")
def load_toxic():
    return DataLoader.load_toxic_ingredients()


@router.post("/all")
def load_all():
    return DataLoader.load_all()