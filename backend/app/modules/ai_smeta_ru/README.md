# AI-Smeta-RU Module

This module is the draft-only architecture shell for the AI-assisted Russian estimating MVP in OpenConstructionERP.

## Final architecture

- api/ exposes placeholder endpoints and schemas.
- domain/ contains pure domain models with no persistence dependency.
- pipeline/ hosts placeholder workflow stages.
- providers/ isolates the module from direct dependency on existing OpenConstructionERP modules.
- adapters/ wraps file-format-specific handling.
- services/ holds placeholder orchestration services.
- review/ captures review status and approval policy scaffolding.
- export/ contains export structure placeholders.
- estimator_package/ holds the combined review package definition.

## MVP boundaries

- No final approved estimates are created in MVP.
- GrandSmeta is treated as the authoritative estimating environment in MVP.
- AI-Smeta-RU prepares an Estimator Package for estimator review and handoff.
- The Estimator Package includes:
  1. GrandSmeta import Excel
  2. Estimator review Excel
  3. designer questions
  4. estimator assumptions
  5. candidate Russian norm mappings
  6. missing data report
  7. pre-expertise self-check report
  8. processing protocol
- After the estimator prepares the estimate in GrandSmeta and receives government expertise comments, a future module named expertise_feedback_engine_ru will analyze those comments and propose solutions.

## Architectural rules

- Existing OpenConstructionERP modules must be accessed through providers and adapters, not directly from business services.
- The architecture language uses “data extraction from scanned documents” instead of OCR.
- No real extraction, norm matching, or Excel generation is implemented yet.
