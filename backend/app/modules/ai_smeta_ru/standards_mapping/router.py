from fastapi import APIRouter

router = APIRouter(tags=["ai_smeta_ru.standards_mapping"])

@router.get("/standards_mapping/status")
async def get_standards_mapping_status() -> dict[str, str]:
    return {"status": "standards_mapping stub"}
