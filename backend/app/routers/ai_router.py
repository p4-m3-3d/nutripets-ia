from fastapi import APIRouter

from app.ai.vector_loader import VectorLoader
from app.ai.search_service import SearchService
from app.ai.rag_service import RagService

from app.schemas.question_schema import QuestionSchema
from app.schemas.search_schema import SearchSchema

router = APIRouter(
    prefix="/ai",
    tags=["Artificial Intelligence"]
)


@router.post("/index")
def create_index():
    return VectorLoader.load_all()


@router.post("/search")
def semantic_search(
    search_data: SearchSchema):
    return SearchService.search(
        search_data.query
    )

@router.post("/ask")
def ask_question(data: QuestionSchema):
    return RagService.ask(
        data.question
    )