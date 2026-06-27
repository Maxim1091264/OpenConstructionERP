from fastapi import APIRouter

router = APIRouter(tags=["ai_smeta_ru.designer_questions"])

@router.get("/designer_questions/status")
async def get_designer_questions_status() -> dict[str, str]:
    return {"status": "designer_questions stub"}
