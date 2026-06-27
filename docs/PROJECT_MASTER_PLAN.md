# AI-Smeta-RU Project Master Plan

## 1. Purpose

This document defines the governance, architecture, and delivery plan for an AI-powered Russian construction estimating assistant based on OpenConstructionERP.

The target system will ingest construction project source materials in multiple formats, extract structured estimating information, map that information to Russian estimating standards, generate estimate content, and support supplier pricing workflows.

The scope includes:
- source document ingestion and processing
- quantity and specification extraction
- Russian estimating structure generation
- norm / price database matching
- supplier RFQ and commercial offer comparison
- export to Excel, GrandSmeta, and SmetaPlan

This plan is intentionally architecture-first and does not modify source code.

---

## 2. System Goal

Build an AI-assisted estimating workflow for the Russian market that can:
- analyze PDF, scanned PDF, DWG, DXF, DOCX, XLSX, RVT, IFC, images, specifications, and BOQ/VOR tables
- extract quantities, materials, equipment, work types, specifications, drawings metadata, rooms/zones/floors, engineering systems, structural elements, openings, reinforcement, finishes, and installation works
- generate Russian VOR, BOQ, estimate positions, and missing-data assumptions
- map to ФСНБ-2022, ГЭСН, ФЕР, and ТЕР
- produce designer / engineer / estimator questions
- create supplier RFQ lists and comparison tables
- support KAC / конъюнктурный анализ цен
- export data to GrandSmeta, SmetaPlan, and Excel

---

## 3. Repository Assessment

The current OpenConstructionERP codebase already contains strong building blocks for this architecture.

### 3.1 Existing modules that can support the architecture

The following modules are directly relevant:

- `backend/app/modules/takeoff`
  - PDF intake, OCR-aware processing, plan reading, measurement extraction, BOQ linkage
  - Strong base for PDF / scanned PDF / drawing-based quantity extraction

- `backend/app/modules/dwg_takeoff`
  - DWG / DXF intake, validation, conversion, entity extraction, annotations
  - Strong base for CAD-based quantity and drawing metadata extraction

- `backend/app/modules/ai_estimator`
  - AI-driven estimating workflow, conversational intake, grouping, matching, and review
  - Strong base for estimate assembly and human-confirmation workflow

- `backend/app/modules/costs`
  - Cost database, cost item search, matching, and regional cost logic
  - Strong base for catalog linkage and rate matching

- `backend/app/modules/boq`
  - BOQ and position management, import/export, and position-level structure
  - Strong base for producing and managing estimate positions

- `backend/app/modules/russia_pack`
  - Regional Russian standards configuration and defaults
  - Strong base for Russian-specific configuration and tax / unit standardization

- `backend/app/modules/supplier_catalogs`
  - Supplier-oriented catalog and price data handling
  - Strong base for supplier data management and pricing workflows

- `backend/app/modules/procurement` and `backend/app/modules/rfq_bidding`
  - RFQ and tendering structures
  - Strong base for supplier RFQ generation and comparison flows

- `backend/app/modules/documents`
  - Document handling and storage foundation
  - Strong base for attachments and source file organization

- `backend/app/modules/bim_hub`, `backend/app/modules/cad`, and `backend/app/modules/pointcloud`
  - BIM and model-related integration layer
  - Useful for future RVT / IFC semantic extraction and model-based quantity workflows

### 3.2 Modules that need extension

The following modules should be extended rather than replaced:

- `takeoff`
  - Add support for DOCX, Excel, scanned-image-based extraction, and more structured field extraction from specifications and tables
  - Extend plan-reading outputs toward Russian estimation objects and VOR-ready structure

- `dwg_takeoff`
  - Add stronger entity-to-estimate mapping for structural, finishing, and install work types
  - Add richer metadata output for rooms, zones, floors, openings, reinforcement, and MEP systems

- `ai_estimator`
  - Extend the conversational intake to support Russian project-type recognition, standards selection, and assumptions generation
  - Add stage gates for regulatory / norm mapping and supplier pricing review

- `costs`
  - Extend cost matching to support Russian cost databases and supplier price databases
  - Add region-aware rate, VAT, currency, and delivery-cost logic

- `boq`
  - Add Russian VOR-focused output structure and export adapters for GrandSmeta and SmetaPlan

- `russia_pack`
  - Expand with richer standard mappings, formulas, and Russian estimating defaults

- `supplier_catalogs` and `procurement`
  - Add support for supplier master data, price validity, alternative products, and commercial-offer comparison logic

### 3.3 New modules that should be created

The architecture will benefit from new modules, even though existing ones provide a foundation.

Recommended new modules:

1. `ai_smeta_ru`
   - Main orchestration module for Russian estimating intelligence
   - Coordinates ingestion, extraction, matching, review, and export workflows

2. `source_ingestion`
   - Unified intake layer for PDFs, images, office documents, CAD/BIM files, and structured tables

3. `document_understanding`
   - OCR, parsing, section classification, table understanding, and document-to-structure pipelines

4. `quantity_normalization`
   - Normalizes extracted quantities into a canonical estimating model

5. `standards_mapping`
   - Maps extracted work items to ФСНБ-2022, ГЭСН, ФЕР, and ТЕР

6. `supplier_pricing_engine`
   - Stores supplier prices, compares offers, manages validity dates, and tracks alternatives

7. `rfq_orchestrator`
   - Creates RFQ lists, collects quotes, and produces comparison tables

8. `export_adapters`
   - Produces Excel, GrandSmeta, and SmetaPlan-ready export structures

9. `assumption_engine`
   - Captures missing-data assumptions and questions to stakeholders

---

## 4. Recommended MVP

The recommended MVP should focus on a narrow but valuable first release.

### MVP scope
- support for PDF, scanned PDF, DWG, DXF, DOCX, XLSX, and image-based source files
- structured extraction of quantities, work types, materials, and basic specifications
- generation of a draft Russian BOQ / estimate structure
- mapping to a limited set of Russian norms and price references
- human-in-the-loop review for assumptions and missing data
- supplier RFQ list generation for selected materials and equipment
- Excel export first, with JSON / CSV structure prepared for later GrandSmeta and SmetaPlan integration

### MVP assumptions
- one project type at a time
- one discipline or a limited number of work packages per run
- explicit human confirmation before applying output to BOQ
- supplier data is initially imported from Excel and manual offers

### MVP success criteria
- the system can ingest a project package and produce a structured draft estimate in under one workflow cycle
- the estimate includes enough traceability to justify each position
- the user can review assumptions and questions before accepting the draft
- the user can export the draft to Excel and start RFQ preparation

---

## 5. Risks and Dependencies

### 5.1 Technical risks
- OCR quality for scanned PDFs and poor-quality images
- inconsistent drawing metadata across CAD/BIM files
- imperfect extraction of quantities from unstructured documents
- ambiguity in norm mapping without strong local reference data

### 5.2 Data risks
- missing specifications and unclear design intent
- incomplete supplier catalogs
- inconsistent units and nomenclature
- differing regional price conditions and delivery assumptions

### 5.3 Integration risks
- dependency on external AI providers or document processing services
- dependency on cost database refresh cycles
- dependency on supplier API availability and data quality

### 5.4 Governance risks
- unclear ownership between estimator, engineer, designer, and procurement
- insufficient review checkpoints for assumptions and norm selection

### 5.5 Key dependencies
- Russian norm / rate reference data
- supplier database content and refresh process
- BIM/CAD conversion tools and their reliability
- AI model performance for document structure understanding

---

## 6. Delivery Roadmap

### Phase 0 — Foundation and governance
- confirm stakeholders, roles, and review workflow
- define the canonical estimating object model
- define Russian norm / standards mapping policy
- define data ownership rules for source files, assumptions, and supplier data

### Phase 1 — Intake and parsing foundation
- integrate PDF / scanned PDF / DWG / DXF / DOCX / XLSX / image ingestion
- implement normalized source artifact storage and metadata extraction
- build initial document classification and section parsing pipeline

### Phase 2 — Quantities and estimate object extraction
- extract quantities, materials, work types, openings, reinforcement, finishes, and installation works
- create normalized estimate objects and traceability links
- support human review and correction of extracted data

### Phase 3 — Russian standards and pricing integration
- map work items to ФСНБ-2022, ГЭСН, ФЕР, and ТЕР
- integrate internal supplier catalog and uploaded price lists
- add price validity, VAT, currency, delivery-cost, and alternative-product logic

### Phase 4 — Review, assumptions, and RFQ workflow
- generate missing-data assumptions and stakeholder questions
- create RFQ lists and comparison tables
- support manual commercial offer ingestion and comparison

### Phase 5 — Export and productization
- add Excel export
- add GrandSmeta and SmetaPlan export structure preparation
- add audit logs, versioning, and approval workflow

---

## 7. Governance Model

### Decision-making structure
- Product owner: overall business ownership and MVP prioritization
- Estimating lead: domain rules, norm mapping, and output quality
- Engineering lead: implementation and system integration
- Procurement lead: supplier data processes and RFQ workflows
- BIM / CAD lead: model and drawing integration quality

### Review gates
1. source intake review
2. extraction quality review
3. norm mapping review
4. supplier pricing review
5. final estimate review

### Change control
- all changes to standards mapping and supplier pricing logic must be versioned
- all generated estimate drafts must preserve source traceability
- assumptions must be explicit and reviewable

---

## 8. Implementation Principles

- AI suggests, humans confirm
- every estimate position must retain source provenance
- no estimate should be generated without explicit assumptions handling
- costs must remain region-, currency-, and VAT-aware
- supplier pricing must be auditable and periodical
- exports must be structured and machine-readable where possible

---

## 9. Recommended Next Step

The immediate next step is to implement the MVP as a layered extension of the existing OpenConstructionERP modules rather than a greenfield replacement. The strongest starting point is:
- reuse `takeoff` and `dwg_takeoff` for source interpretation
- reuse `ai_estimator` for workflow orchestration
- reuse `costs` and `boq` for estimate assembly
- create a new Russian estimating orchestration module and supplier pricing module on top of this foundation
