# AI-Smeta-RU MVP Roadmap

## 1. MVP Objective

Deliver a first-version AI-assisted Russian estimating workflow that can ingest a limited set of project source files, extract structured estimating data, create a draft VOR / BOQ-style estimate structure, highlight missing data, and export a reviewable Excel output.

The MVP is not intended to produce a fully approved final estimate automatically. It is designed to reduce manual effort, surface assumptions clearly, and create a human-reviewed draft that can be refined by estimators.

---

## 2. What Is Included in MVP

The MVP will include the following capabilities:

- upload project source files
- classify uploaded documents by project discipline
- process supported source formats:
  - PDF
  - scanned PDF
  - DOCX
  - XLSX
  - DWG/DXF as research integration only
- extract tables, specifications, and basic quantity-related content
- extract quantities and materials where possible
- normalize extracted content into a draft VOR / estimate structure
- detect missing data and unresolved items
- generate assumptions and questions for the estimator / designer / engineer
- map extracted work items to candidate Russian norms using GESN / FER suggestions only
- export a reviewable Excel package and prepare GrandSmeta import-ready draft data
- support supplier pricing using uploaded Excel price lists and manual offers

---

## 3. What Is Excluded from MVP

The following are explicitly out of scope for the first release:

- fully automatic final estimate approval
- automatic final norm selection without human review
- live supplier website scraping
- external supplier API integrations
- full BIM semantic interpretation for RVT / IFC
- end-to-end production-grade DWG/DXF takeoff automation
- full GrandSmeta or SmetaPlan direct export in the first release
- fully automated procurement workflow
- full multi-discipline end-to-end estimation without human review

---

## 4. Supported Source Formats in MVP

### 4.1 Included in MVP

- PDF
- scanned PDF
- DOCX
- XLSX

### 4.2 Research integration only

- DWG / DXF

DWG and DXF files will be supported as a research integration in MVP. The goal is to test whether basic drawing metadata and geometry can be used to improve estimating drafts, but these formats will not be treated as a full production workflow in the first release.

---

## 5. First Supported Project Disciplines

The first supported disciplines will be:

- AR — архитектурные работы / architectural works
- KR — конструкции / structures
- OV — отопление и вентиляция / heating and ventilation
- VK — водоснабжение и канализация / water supply and sewerage
- EOM — electrical, low-current, and related systems / electrical and communications works

These disciplines are a practical first set because they cover common Russian estimating workflows and are likely to appear in typical design packages.

---

## 6. Core MVP Workflow

The MVP workflow will be:

1. Upload source files
   - project documents, specifications, typical tables, drawings, and price lists

2. Classify documents by discipline
   - determine whether a file belongs to AR, KR, OV, VK, or EOM

3. Extract tables and specifications
   - extract structured tables from DOCX and XLSX
   - extract specification-related content from documents
   - identify quantities and unit fields where present

4. Extract quantities and materials
   - detect quantities, units, material descriptions, and work types from supported files
   - record source provenance for every extracted item

5. Normalize into VOR
   - convert extracted content into a normalized draft VOR / estimate structure
   - produce draft estimate positions with descriptions, units, quantities, and basic traceability

6. Detect missing data
   - identify missing quantity fields, missing units, missing materials, missing specifications, and unresolved references

7. Generate assumptions and questions
   - create explicit assumptions for uncertain items
   - create follow-up questions for designers, engineers, estimators, or procurement staff

8. Map to candidate Russian norms
   - suggest GESN / FER candidates for each item
   - mark them as candidate suggestions only, not final approved norms

9. Export to Excel and GrandSmeta
   - provide an Excel export of the draft estimate with traceability and assumption notes
   - prepare GrandSmeta import-ready draft data for estimator review and finalization in GrandSmeta

---

## 7. Russian Standards Scope

### 7.1 Included in MVP

- GESN / FER mapping as candidate suggestions only
- basic mapping of extracted work items to likely Russian norm families
- explicit human review before any final norm assignment

### 7.2 Excluded from MVP

- automatic final estimate approval based on norms
- automatic final norm selection
- full regulatory-compliance validation engine in the first release

---

## 8. Supplier Pricing Scope

### 8.1 Included in MVP

- uploaded supplier Excel price lists
- manual supplier offers
- simple comparison table for selected materials and equipment

### 8.2 Excluded from MVP

- live website scraping
- external supplier APIs
- automated real-time price refresh pipelines

---

## 9. Required New Modules

The MVP should introduce the following new modules or subsystems:

1. `ai_smeta_ru`
   - main orchestration module for the MVP workflow
   - coordinates ingestion, normalization, review, and export

2. `source_ingestion`
   - handles upload and routing of accepted source files

3. `document_understanding`
   - performs document classification, scanned document extraction, table extraction, and specification parsing

4. `quantity_normalization`
   - turns extracted data into normalized VOR / estimate objects

5. `standards_mapping`
   - provides candidate GESN / FER mapping suggestions

6. `assumption_engine`
   - creates missing-data assumptions and follow-up questions

7. `supplier_pricing_engine`
   - stores and compares uploaded supplier price lists and manual offers

8. `grandsmeta_excel_export_ru`
   - produces reviewable Excel export structures and prepares GrandSmeta import-ready output

9. `expertise_comments_analyzer_ru`
   - analyzes government expertise comments and links them to draft estimate items, assumptions, and issues

---

## 10. Existing OpenConstructionERP Modules to Reuse

The MVP should reuse the following existing OpenConstructionERP modules wherever possible:

- `backend/app/modules/takeoff`
  - for PDF and scanned-PDF processing, document parsing, and measurement extraction

- `backend/app/modules/dwg_takeoff`
  - for DWG / DXF research integration and drawing-related experimentation

- `backend/app/modules/ai_estimator`
  - for workflow orchestration, human-review checkpoints, and estimate drafting behavior

- `backend/app/modules/costs`
  - for cost-item matching and pricing logic

- `backend/app/modules/boq`
  - for BOQ and estimate position structure

- `backend/app/modules/russia_pack`
  - for Russian regional defaults and standards-related configuration

- `backend/app/modules/supplier_catalogs`
  - for supplier catalog storage and price data foundations

- `backend/app/modules/documents`
  - for source file storage and versioning

- `backend/app/modules/grandsmeta_export`
  - for preparing GrandSmeta import-ready deliverables

- `backend/app/modules/procurement` and `backend/app/modules/rfq_bidding`
  - for future RFQ and supplier comparison workflows

- `backend/app/modules/documents`
  - for source file storage and versioning

---

## 11. Step-by-Step Implementation Phases

### Phase 0 — Project preparation and governance

Objective:
- define scope, roles, review rules, and data ownership

Included work:
- confirm MVP disciplines and file types
- define the canonical VOR / estimate object model
- define review gate rules
- define assumptions and question handling policy

Acceptance criteria:
- MVP scope is agreed
- object model draft is documented
- review workflow is defined
- file types and disciplines are confirmed

Risks:
- unclear ownership between estimator, engineer, and procurement roles
- overly broad scope

---

### Phase 1 — Source ingestion and document routing

Objective:
- support upload and classification of supported source files

Included work:
- implement upload endpoints and storage for supported documents
- classify documents by discipline
- route files to appropriate processing modules

Acceptance criteria:
- PDF, scanned PDF, DOCX, and XLSX uploads are accepted
- files are stored with metadata and version info
- basic discipline classification is available for AR, KR, OV, VK, and EOM

Risks:
- inconsistent naming or document structure
- classification errors for mixed-content packages

---

### Phase 2 — Document understanding and extraction

Objective:
- extract tables, specifications, and key estimating data

Included work:
- parse DOCX and XLSX tables
- extract specifications and sections from documents
- process PDF text and scanned document extraction output
- extract candidate quantities and material references

Acceptance criteria:
- tables and specifications can be extracted into structured output
- quantities and material references are surfaced as candidate estimate items
- extracted content is traceable to source files

Risks:
- scanned document extraction quality may be inconsistent
- poor table structure in source documents

---

### Phase 3 — Quantity normalization and VOR drafting

Objective:
- normalize extracted data into a draft VOR / estimate structure

Included work:
- convert extracted content into a canonical estimate-object model
- create draft positions with description, unit, quantity, and source link
- create a draft VOR structure for review

Acceptance criteria:
- draft VOR items can be generated from extracted source data
- each item retains source provenance
- quantities and units are normalized where possible

Risks:
- inconsistent units and naming conventions
- incomplete or ambiguous quantity extraction

---

### Phase 4 — Assumptions, questions, and missing-data handling

Objective:
- make uncertainty explicit and reviewable

Included work:
- detect missing values and unresolved references
- generate assumptions and questions for stakeholders
- flag items needing estimator review

Acceptance criteria:
- missing-data issues are visible in the draft output
- assumptions and follow-up questions are generated for unresolved items
- unresolved items are not silently accepted

Risks:
- too much ambiguity may overwhelm the user
- missing information may not be easy to categorize

---

### Phase 5 — Russian norm mapping suggestions

Objective:
- provide candidate GESN / FER mappings for draft estimate items

Included work:
- create a candidate norm mapping layer
- map items to likely GESN / FER families with confidence scores
- mark outputs as suggestion-only

Acceptance criteria:
- draft items receive candidate norm suggestions
- suggestions are clearly marked as non-final
- estimators can review and override suggestions

Risks:
- lack of authoritative norm reference data
- poor mapping quality for mixed or incomplete descriptions

---

### Phase 6 — Supplier pricing integration

Objective:
- support supplier price list import and manual offer handling

Included work:
- import supplier Excel price lists
- capture manual commercial offers
- compare selected items and present a simple comparison table

Acceptance criteria:
- supplier Excel uploads are accepted and normalized
- manual offers can be recorded for selected estimate items
- comparison output is available for review

Risks:
- inconsistent supplier naming and units
- repeated manual data entry burden

---

### Phase 7 — Excel export and review workflow

Objective:
- deliver a usable first export for estimator review

Included work:
- export draft VOR / estimate objects to Excel
- include assumptions, questions, and source references
- make the output suitable for review and iteration

Acceptance criteria:
- Excel export is generated successfully
- output includes draft positions and traceability
- assumptions and questions are included in the export

Risks:
- export format may need iterative refinement based on estimator feedback

---

## 12. Acceptance Criteria by Phase

| Phase | Acceptance criteria |
|---|---|
| Phase 0 | Scope, disciplines, model, and workflow are agreed |
| Phase 1 | Supported files upload and are routed correctly |
| Phase 2 | Structured extraction works for DOCX, XLSX, PDF, and scanned PDF |
| Phase 3 | Draft VOR positions are created with provenance |
| Phase 4 | Missing-data assumptions and questions are generated |
| Phase 5 | Candidate GESN / FER mappings are available and reviewable |
| Phase 6 | Supplier Excel lists and manual offers are handled |
| Phase 7 | Excel output is usable by estimators |

---

## 13. Risks

- scanned document extraction quality may be inconsistent
- source documents may have weak structure or inconsistent formatting
- units and descriptions may differ across source files
- Russian norm mapping may require domain-specific reference data
- supplier price lists may be incomplete or inconsistent
- AI extraction quality may require iterative tuning and reviewer feedback
- the MVP may expand beyond its intended scope unless strict governance is maintained

---

## 14. Open Questions

1. Which Russian norm reference data source will be used for candidate mapping in MVP?
2. Which disciplines and work packages are highest priority for the first release?
3. Should supplier price handling be limited to Excel import only, or include manual offer entry from the start?
4. What minimum Excel export structure is required by estimators?
5. How much of the document classification should be rule-based versus AI-based?
6. What level of traceability is required for every extracted estimate item?
7. Should DWG/DXF remain a research-only integration in the MVP, or should a minimal pilot be included?
8. What approval workflow is required before a draft estimate is considered review-ready?
