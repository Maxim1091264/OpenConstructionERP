from fastapi import APIRouter

router = APIRouter(tags=["ai_smeta_ru.assumption_engine"])

@router.get("/assumption_engine/status")
async def get_assumption_engine_status() -> dict[str, str]:
    return {"status": "assumption_engine stub"}
