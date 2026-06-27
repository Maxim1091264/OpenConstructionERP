from fastapi import APIRouter

router = APIRouter(tags=["ai_smeta_ru.common"])

@router.get("/common/status")
async def get_common_status() -> dict[str, str]:
    return {"status": "ai_smeta_ru common stub"}
