from fastapi import APIRouter

router = APIRouter(tags=["ai_smeta_ru.completeness_checker"])

@router.get("/completeness_checker/status")
async def get_completeness_checker_status() -> dict[str, str]:
    return {"status": "completeness_checker stub"}
