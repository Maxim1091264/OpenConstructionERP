from fastapi import APIRouter

router = APIRouter(tags=["ai_smeta_ru.grandsmeta_excel_export"])

@router.get("/grandsmeta_excel_export/status")
async def get_grandsmeta_excel_export_status() -> dict[str, str]:
    return {"status": "grandsmeta_excel_export stub"}
