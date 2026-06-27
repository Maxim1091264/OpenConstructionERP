from pydantic import BaseModel


class GrandsmetaExcelExportSchema(BaseModel):
    name: str = "grandsmeta_excel_export"
