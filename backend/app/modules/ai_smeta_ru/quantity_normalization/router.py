from fastapi import APIRouter

router = APIRouter(tags=["ai_smeta_ru.quantity_normalization"])

@router.get("/quantity_normalization/status")
async def get_quantity_normalization_status() -> dict[str, str]:
    return {"status": "quantity_normalization stub"}
