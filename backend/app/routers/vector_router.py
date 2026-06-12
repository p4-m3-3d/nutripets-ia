from fastapi import APIRouter

from app.ai.vector_loader import VectorLoader

router = APIRouter(
prefix="/vector",
tags=["Vector Database"]
)

@router.post("/load")
def load_vectors():
    return VectorLoader.load_all()
