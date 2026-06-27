from fastapi import APIRouter

router = APIRouter(tags=["ai_smeta_ru.estimator_package"])

@router.get("/estimator_package/status")
async def get_estimator_package_status() -> dict[str, str]:
    return {"status": "estimator_package stub"}
