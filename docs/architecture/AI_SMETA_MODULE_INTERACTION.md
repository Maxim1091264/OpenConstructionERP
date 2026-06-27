# AI-Smeta-RU Module Interaction Architecture

## Purpose

This document describes the final architecture shape for the AI-Smeta-RU module.
The intent is to keep business services independent from direct dependency on
existing OpenConstructionERP modules while preparing a draft estimator package.

## MVP boundaries

- AI-Smeta-RU does not create final approved estimates.
- GrandSmeta is the authoritative estimating environment in MVP.
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

## Future extension

After the estimator prepares the estimate in GrandSmeta and receives government expertise comments, a future module named expertise_feedback_engine_ru will analyze the comments and propose solutions.

## Architectural rule

Existing OpenConstructionERP modules must be accessed through providers and adapters,
not directly from business services.

## Non-user-facing language note

The architecture language uses "data extraction from scanned documents" rather than the term OCR.
