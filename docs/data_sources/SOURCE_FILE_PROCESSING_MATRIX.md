# Source File Processing Matrix

## 1. Purpose

This matrix defines how the AI-Smeta-RU adaptation should process each source file type and what output should be expected from each pipeline.

---

## 2. Processing Matrix

| Source type | Current repository support | Primary extraction targets | Recommended processing approach | Expected output artifacts | Gaps / extension needs | Priority |
|---|---|---|---|---|---|---|
| PDF | Strong foundation in `takeoff` | quantities, dimensions, drawings, tables, notes | parse text, detect tables, run OCR if needed, run geometry-aware extraction | structured quantities, measurements, document metadata | scanned PDF quality and better section understanding | High |
| Scanned PDF | Partial via OCR and takeoff pipeline | text, tables, dimensions, room annotations | OCR + layout analysis + classification | OCR text, extracted quantities, reviewable candidate objects | robustness and confidence scoring | High |
| DWG | Strong foundation in `dwg_takeoff` | layers, entities, geometry, metadata | convert / parse, extract entity groups, infer work objects | CAD entities, layers, drawing metadata, candidate quantities | mapping to estimate objects and Russian work types | High |
| DXF | Strong foundation in `dwg_takeoff` | geometry, layers, text, blocks | parse entities and attributes | structured geometry and drawing metadata | semantic mapping to work packages | High |
| Word / DOCX | Limited today | specifications, scope notes, method statements, tables | parse sections, tables, and headings | structured specifications and scope objects | better table understanding and section classification | High |
| Excel / XLSX | Existing import and catalog workflows | BOQ tables, schedules, quantity sheets, supplier price lists | parse tabular data, normalize units, detect headers | normalized rows and estimate tables | schema inference and mixed-format handling | High |
| RVT | Partial / integration-oriented | model elements, families, categories, metadata | use BIM conversion / model ingestion pipeline | model element inventory and quantity candidates | semantic mapping to estimating objects | Medium |
| IFC | Partial / integration-oriented | building elements, spaces, systems, properties | parse model entities and properties | elements, properties, quantities, spatial structure | mapping to norms and estimate items | Medium |
| Images | Partial through OCR and vision-based takeoff | photos, details, labels, site conditions | OCR, vision classification, object recognition | extracted labels, dimensions, and candidate objects | quality control and confidence scoring | Medium |
| Specifications | Needs structured layer | materials, products, system requirements, methods | classify clauses and extract targets | structured spec objects with references | normative terminology and cross-linking | High |
| BOQ / VOR tables | Existing BOQ and takeoff foundations | line items, quantities, units, descriptions | parse and normalize rows into estimate positions | canonical BOQ / VOR draft rows | Russian norm alignment and mapping | High |

---

## 3. Extraction Targets by File Type

### 3.1 Quantities
Supported by:
- PDF / scanned PDF
- DWG / DXF
- Excel tables
- IFC / RVT models where geometry is available

### 3.2 Materials and equipment
Supported by:
- specifications
- DOCX / Word documents
- Excel schedules
- supplier price lists
- BIM model properties where available

### 3.3 Work types
Supported by:
- BOQ / VOR tables
- specifications
- drawings and markups
- text classification over project documents

### 3.4 Rooms / zones / floors
Supported by:
- BIM and CAD model metadata
- architectural drawings
- room schedules in Excel

### 3.5 Engineering systems, openings, reinforcement, finishes, installation works
Supported by:
- BIM / CAD model extraction
- specifications and detail sheets
- schedule tables and technical notes

---

## 4. Recommended Processing Pipeline

Each source file should pass through the same five-stage processing pattern:

1. Intake
   - store the file, metadata, and version
2. Structural parsing
   - extract text, tables, geometry, or model entities
3. Semantic classification
   - identify work items, materials, systems, spaces, and metadata types
4. Normalization
   - convert the content into the canonical estimating model
5. Review
   - expose unresolved items, assumptions, and follow-up questions to the estimator

---

## 5. Output Model per Source Type

| Source type | Output structure |
|---|---|
| PDF / scanned PDF | measurements, candidate positions, OCR text, page-level metadata |
| DWG / DXF | entities, layers, blocks, geometry metadata, candidate quantities |
| DOCX | sections, tables, specification objects |
| XLSX | rows, columns, normalized quantities, supplier price rows |
| RVT / IFC | element inventory, properties, quantities, spatial relationships |
| Images | OCR text, detected labels, candidate objects |

---

## 6. Prioritization Logic

The MVP should prioritize source types that are most common in early Russian estimating workflows and that already have the best repository support:

1. PDF and scanned PDF
2. DWG and DXF
3. DOCX and XLSX
4. BOQ / VOR tables
5. IFC and RVT
6. images and photo-based detail extraction

---

## 7. Governance Notes

- every extraction result must be traceable to the original source artifact
- unresolved extraction should be surfaced as an assumption or a question
- source files should be versioned and reviewable
- no final estimate position should be accepted without a review step
