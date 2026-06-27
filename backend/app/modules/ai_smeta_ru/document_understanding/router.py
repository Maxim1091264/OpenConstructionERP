from fastapi import APIRouter

router = APIRouter(tags=["ai_smeta_ru.document_understanding"])

@router.get("/document_understanding/status")
async def get_document_understanding_status() -> dict[str, str]:
    return {"status": "document_understanding stub"}
