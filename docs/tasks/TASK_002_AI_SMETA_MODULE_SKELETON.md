# TASK 002 — AI SMETA RU Module Skeleton

## 1. Goal

Create the skeleton package for the Russian estimating MVP module in OpenConstructionERP. This task is focused on scaffolding a clean backend module structure under `backend/app/modules/ai_smeta_ru` without implementing full production business logic.

The generated skeleton is intended to support:
- draft estimate ingestion and review workflows
- source extraction and normalization
- completeness checking and follow-up questions
- estimator assumptions
- Russian norm candidate suggestions
- GrandSmeta-ready export and estimator package assembly

This task explicitly does not implement final estimate approval, full government expertise automation, or complete Russian pricing logic.

---

## 2. Generated Skeleton Structure

The architecture has been refined into the following structure:

- `backend/app/modules/ai_smeta_ru/`
  - `api/`
  - `common/`
  - `domain/`
  - `pipeline/`
  - `providers/`
  - `adapters/`
  - `services/`
  - `review/`
  - `export/`
  - `estimator_package/`
  - `tests/`

The module contains placeholder domain models, pipeline stages, provider interfaces, adapter placeholders, service shells, review scaffolding, export stubs, and an Estimator Package definition.

---

## 3. Architecture Principles

The final architecture clearly states that:
- MVP does not create final approved estimates.
- GrandSmeta is the authoritative estimating environment in MVP.
- AI-Smeta-RU prepares an Estimator Package.
- The Estimator Package includes:
  1. GrandSmeta import Excel
  2. Estimator review Excel
  3. designer questions
  4. estimator assumptions
  5. candidate Russian norm mappings
  6. missing data report
  7. pre-expertise self-check report
  8. processing protocol
- After the estimator prepares the estimate in GrandSmeta and receives government expertise comments, a future module `expertise_feedback_engine_ru` will analyze the comments and propose solutions.
- Existing OpenConstructionERP modules are accessed through providers and adapters, not directly from business services.
- The architecture uses “data extraction from scanned documents” rather than OCR terminology.

---

## 4. Module Manifest

The module manifest registers `oe_ai_smeta_ru` with the module loader, depending on:
- `oe_ai_estimator`
- `oe_russia_pack`
- `oe_supplier_catalogs`
- `oe_costs`
- `oe_boq`

The module is created disabled by default (`enabled=False`) and not auto-installed.

---

## 5. Next Work Items

1. Define the internal data model for the AI SMETA RU workflow.
2. Add schema and repository definitions for source artifacts, extracted objects, quantities, work items, norm candidates, and review issues.
3. Wire the module into the existing module loader and API routing once ready.
4. Implement stub service methods for data ingestion, review preparation, and GrandSmeta export.
5. Create task-specific tests verifying route mountability and schema validation.
