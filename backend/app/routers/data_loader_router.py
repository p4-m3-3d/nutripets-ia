from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.data_loader import DataLoader

router = APIRouter(
    prefix="/loader",
    tags=["Data Loader"]
)


@router.post("/recipes", status_code=status.HTTP_200_OK)
def load_recipes(db: Session = Depends(get_db)):
    return DataLoader.load_recipes(db=db)


@router.post("/advice", status_code=status.HTTP_200_OK)
def load_advice(db: Session = Depends(get_db)):
    return DataLoader.load_advice(db=db)


@router.post("/faq", status_code=status.HTTP_200_OK)
def load_faq(db: Session = Depends(get_db)):
    return DataLoader.load_faq(db=db)


@router.post("/toxic", status_code=status.HTTP_200_OK)
def load_toxic(db: Session = Depends(get_db)):
    return DataLoader.load_toxic_ingredients(db=db)


@router.post("/all", status_code=status.HTTP_200_OK)
def load_all(db: Session = Depends(get_db)):
    return DataLoader.load_all(db=db)