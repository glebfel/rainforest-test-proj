from fastapi import APIRouter

from src.schemas import OutputQuestionSchema

products_router = APIRouter(tags=["Math Solver"])


@products_router.post("/get_answer")
def get_answer(
) -> OutputQuestionSchema:
    pass