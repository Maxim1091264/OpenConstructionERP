# TASK 001 — RU Data Extraction Layer

## 1. Goal

Design and document the first implementation task for the Russian estimating layer in OpenConstructionERP.

The task covers the initial data-extraction and structuring pipeline for Russian estimating workflows. Its purpose is to help an estimator ingest project source files, structure the information, detect missing data, generate questions for designers and engineers, create assumptions for estimator review, suggest Russian norm candidates, check government expertise readiness, and export a reviewable Excel package.

This task is intentionally limited to:
- data extraction
- data structuring
- completeness checking
- questions to designers
- assumptions for estimator review
- Russian GESN / FER / TER candidate mapping
- government expertise readiness checks
- Excel output for estimator review

No source code implementation is included in this task.

---

## 2. User Workflow for Estimator

The estimator workflow for this task is:

1. Upload project source files
   - PDF
   - scanned PDF
   - DOCX
   - XLSX
   - DWG/DXF as research-only input

2. Review the intake package
   - confirm the project discipline and source set
   - review initial document classification

3. Run extraction and structuring
   - extract tables, specifications, quantities, materials, and work descriptions
   - structure the extracted information into a normalized internal model

4. Review completeness results
   - inspect missing data issues
   - review unresolved quantities and missing specifications

5. Generate questions for designers / engineers
   - produce a list of targeted questions for follow-up

6. Generate assumptions for estimator review
   - create explicit assumptions for ambiguous or missing items

7. Review norm candidates
   - inspect suggested GESN / FER / TER mappings as candidate suggestions only

8. Review expertise readiness checks
   - inspect whether the current draft is ready for government expertise review
   - see which issues still block readiness

9. Export Excel review package
   - export a structured spreadsheet for estimator review

---

## 3. Input Formats

### 3.1 PDF
Supported for:
- text extraction
- table detection where possible
- document section recognition
- quantity and specification extraction where present

### 3.2 Scanned PDF
Supported for:
- scanned document extraction for image-based sources
- layout analysis
- table recognition where feasible
- quantity and specification candidate extraction

### 3.3 DOCX
Supported for:
- section parsing
- specification extraction
- table extraction
- work description and quantity table understanding

### 3.4 XLSX
Supported for:
- BOQ-style tables
- quantity tables
- specification schedules
- supplier price tables for later extension

### 3.5 DWG / DXF
Supported only as research integration in this task.

DWG / DXF files may be used to:
- extract drawing metadata
- detect basic geometry-related context
- improve confidence for quantity-related interpretations

They are not treated as a full production automation path in this task.

---

## 4. Output Data Model

The implementation task should define a normalized internal data model for downstream review and export.

### 4.1 SourceArtifact
Represents a single ingested source file.

Required fields:
- id
- project_id
- original_filename
- source_type
- storage_path or reference
- discipline
- uploaded_at
- checksum or file hash
- metadata
- provenance

### 4.2 ExtractedObject
Represents a unit of information extracted from a source artifact.

Required fields:
- id
- source_artifact_id
- object_type
- raw_text
- normalized_text
- confidence
- page_reference or location
- linked_work_item_id

### 4.3 QuantityItem
Represents a quantity or measurement derived from the source.

Required fields:
- id
- work_item_id
- quantity
- unit
- unit_normalized
- measurement_basis
- source_reference
- confidence

### 4.4 WorkItem
Represents a candidate estimating work item.

Required fields:
- id
- discipline
- description
- unit
- quantities
- source_links
- status
- estimated_category

### 4.5 MaterialItem
Represents a material referenced by the work item.

Required fields:
- id
- work_item_id
- material_name
- unit
- quantity_reference
- source_reference
- confidence

### 4.6 EquipmentItem
Represents equipment referenced by the work item.

Required fields:
- id
- work_item_id
- equipment_name
- quantity_reference
- unit
- source_reference
- confidence

### 4.7 NormCandidate
Represents a candidate Russian norm mapping suggestion.

Required fields:
- id
- work_item_id
- norm_family
- norm_code
- confidence
- source_basis
- review_status

### 4.8 MissingDataIssue
Represents missing or uncertain information that blocks a clean estimate draft.

Required fields:
- id
- work_item_id
- issue_type
- description
- severity
- source_reference

### 4.9 DesignerQuestion
Represents a follow-up question to a designer or engineer.

Required fields:
- id
- work_item_id
- question_text
- target_role
- priority
- created_at

### 4.10 EstimatorAssumption
Represents an explicit assumption created for estimator review.

Required fields:
- id
- work_item_id
- assumption_text
- rationale
- confidence
- review_status

### 4.11 ExpertiseCheckIssue
Represents a government expertise readiness issue or blocker.

Required fields:
- id
- work_item_id
- issue_type
- description
- severity
- recommendation

---

## 5. Module Responsibilities

### 5.1 document_understanding_ru
Responsibilities:
- ingest and classify supported source files
- extract text, tables, specifications, and layout hints
- identify the document’s likely discipline
- preserve source provenance

Scope in this task:
- PDF / scanned PDF / DOCX / XLSX parsing
- document discipline classification
- extraction of structured content for estimating review

### 5.2 quantity_normalization_ru
Responsibilities:
- normalize extracted content into estimate-ready units and quantities
- create draft quantity items and work items
- structure content into canonical estimating objects

Scope in this task:
- quantity normalization
- unit normalization
- basic work item construction

### 5.3 completeness_checker_ru
Responsibilities:
- detect missing quantities, missing units, missing materials, missing specifications, and unresolved values
- produce completeness issues that must be reviewed

Scope in this task:
- incomplete-data detection
- severity scoring
- review-ready issue lists

### 5.4 assumption_engine_ru
Responsibilities:
- generate assumptions for ambiguous or missing items
- create explicit assumptions for estimator review
- preserve assumptions as reviewable objects

Scope in this task:
- assumption generation
- rationale capture
- review status tracking

### 5.5 standards_mapping_ru
Responsibilities:
- map extracted work items to candidate Russian standards
- suggest GESN / FER / TER candidates
- mark results as candidate suggestions only

Scope in this task:
- candidate norm mapping
- confidence handling
- review flags for human approval

### 5.6 pre_expertise_self_check_ru
Responsibilities:
- evaluate whether the current draft is likely ready for government expertise submission
- identify missing information and readiness blockers
- produce expertise issues and recommendations

Scope in this task:
- expertise readiness checks
- blocker detection
- checklist-style issue reporting

### 5.7 grandsmeta_excel_export_ru
Responsibilities:
- create an Excel export for estimator review
- prepare GrandSmeta import-ready draft data
- include extracted items, assumptions, questions, norm candidates, and expertise issues

Scope in this task:
- reviewable Excel workbook structure
- sheet design for extracted data and issues

### 5.8 expertise_comments_analyzer_ru
Responsibilities:
- analyze government expertise comments and link them to draft estimate items, norms, assumptions, and issues
- identify comment-driven revision candidates
- preserve comment provenance for review

Scope in this task:
- expertise comment parsing
- item linkage and recommendation generation
- review traceability reporting

---

## 6. Existing OpenConstructionERP Modules to Reuse

The following existing modules should be reused where possible:

- `backend/app/modules/takeoff`
  - PDF and scanned-PDF extraction foundation
  - measurement parsing and document understanding

- `backend/app/modules/dwg_takeoff`
  - DWG / DXF research integration
  - drawing metadata and basic geometry context

- `backend/app/modules/documents`
  - storage and versioning of uploaded source files

- `backend/app/modules/ai_estimator`
  - review workflow concepts, human-confirmation patterns, and structured drafting flow

- `backend/app/modules/boq`
  - BOQ and position structure as a downstream target for normalized work items

- `backend/app/modules/costs`
  - cost-item matching and rate-related downstream use cases

- `backend/app/modules/russia_pack`
  - Russian regional defaults and standards-related configuration

- `backend/app/modules/supplier_catalogs`
  - future supplier price integration support, even if not implemented in this task

---

## 7. New Files and Folders to Create

The task should introduce the following new structure:

- `backend/app/modules/document_understanding_ru/`
- `backend/app/modules/quantity_normalization_ru/`
- `backend/app/modules/completeness_checker_ru/`
- `backend/app/modules/assumption_engine_ru/`
- `backend/app/modules/standards_mapping_ru/`
- `backend/app/modules/pre_expertise_self_check_ru/`
- `backend/app/modules/grandsmeta_excel_export_ru/`
- `backend/app/modules/expertise_comments_analyzer_ru/`

Suggested files:

- `manifest.py`
- `models.py`
- `schemas.py`
- `service.py`
- `router.py`
- `repository.py`
- `README.md` or task-local documentation

A shared internal package may also be created for common data structures if needed.

---

## 8. Step-by-Step Implementation Plan

### Phase 1 — Define the domain model

Objective:
- define the canonical internal objects for this task

Work:
- finalize the data model for source artifacts, extracted objects, quantity items, work items, materials, equipment, norm candidates, missing-data issues, designer questions, assumptions, and expertise issues
- define validation rules and field requirements

Acceptance criteria:
- the data model is documented and approved
- each object has clear required fields and lifecycle status

---

### Phase 2 — Source ingestion and classification

Objective:
- create the intake layer for supported formats

Work:
- define storage and routing for PDF, scanned PDF, DOCX, XLSX, and DWG/DXF research input
- define discipline classification rules for AR, KR, OV, VK, and EOM
- preserve file provenance and metadata

Acceptance criteria:
- supported files are routed to the correct handler
- document discipline is assigned or flagged for review
- source provenance is retained

---

### Phase 3 — Extraction pipeline

Objective:
- extract structured information from supported source files

Work:
- implement parsing for DOCX and XLSX tables and sections
- implement PDF and scanned document extraction entry points
- create an extraction layer that outputs raw structured objects

Acceptance criteria:
- structure can be extracted from DOCX and XLSX
- PDF and scanned PDF content can be converted into candidate extracted objects
- source references are retained for each extracted object

---

### Phase 4 — Normalization and structuring

Objective:
- create normalized work items and quantity items from extracted data

Work:
- normalize units and quantities where possible
- link extracted objects to work items
- create initial material and equipment candidates when found

Acceptance criteria:
- extracted content becomes structured work items and quantity items
- each item can be traced to its source artifact

---

### Phase 5 — Completeness and issue detection

Objective:
- identify missing data and review blockers

Work:
- detect missing quantities, missing units, missing materials, unresolved specifications, and incomplete work descriptions
- create MissingDataIssue records

Acceptance criteria:
- missing-data issues are surfaced in a reviewable list
- severity levels are assigned

---

### Phase 6 — Questions and assumptions generation

Objective:
- create actionable follow-up items for stakeholders

Work:
- generate DesignerQuestion objects for missing design details
- generate EstimatorAssumption objects for ambiguous items

Acceptance criteria:
- questions are grouped by target role and priority
- assumptions are explicit and reviewable

---

### Phase 7 — Russian norm candidate mapping

Objective:
- provide candidate GESN / FER / TER suggestions

Work:
- create a candidate mapping layer for Russian norms
- assign confidence and rationale
- mark all outputs as candidate suggestions only

Acceptance criteria:
- work items receive candidate norm suggestions
- suggestions are clearly marked as non-final

---

### Phase 8 — Expertise readiness checks

Objective:
- assess whether a draft is ready for expertise review

Work:
- create expertise-readiness checks based on missing data and unresolved issues
- produce ExpertiseCheckIssue records with recommendations

Acceptance criteria:
- the system can provide a readiness summary and a list of blockers
- readiness issues are distinct from norm suggestions

---

### Phase 9 — Excel export for estimator review

Objective:
- export a review-ready workbook

Work:
- define workbook sheets for extracted items, quantities, assumptions, questions, norm candidates, and expertise issues
- include traceability and review status

Acceptance criteria:
- Excel export is generated successfully
- estimator can review the output without needing to inspect raw source files first

---

## 9. Acceptance Criteria

The task is complete when the following are achieved:

- supported source formats can be ingested and classified
- extracted information is structured into normalized objects
- missing-data issues are detected and surfaced
- questions and assumptions are generated for estimator review
- candidate Russian norm mappings are available for review
- government expertise readiness issues are surfaced
- an Excel review package can be exported
- no final norm assignment or final approval happens automatically without estimator review

---

## 10. Risks

- scanned document extraction quality may be inconsistent
- document structures may be inconsistent across source files
- table parsing may be incomplete for complex financial or specification tables
- unit normalization may be ambiguous
- Russian norm mapping may require high-quality reference data
- expertise requirements may vary by project type and region
- the system may over-promise automation if it is not clearly scoped as review-first

---

## 11. What Must NOT Be Automated Without Estimator Approval

The following must remain human-reviewed and must not be auto-approved:

- final Russian norm assignment
- final estimate approval
- final government expertise readiness declaration
- final assumption acceptance
- final question resolution
- any change that materially alters quantity interpretation without estimator review
- any replacement of source-derived data with inferred values without visible traceability

The system should always present recommendations, not authoritative decisions, unless a later phase explicitly introduces human-confirmed automation.
