from app.core.module_loader import ModuleManifest

manifest = ModuleManifest(
    name="oe_ai_smeta_ru",
    version="0.1.0",
    display_name="AI SMETA RU",
    description=(
        "Skeleton module for AI-assisted Russian estimating draft workflows "
        "and GrandSmeta handoff preparation."
    ),
    author="OpenConstructionERP Core Team",
    category="core",
    depends=[
        "oe_ai_estimator",
        "oe_russia_pack",
        "oe_supplier_catalogs",
        "oe_costs",
        "oe_boq",
    ],
    auto_install=False,
    enabled=False,
)
