# ADR 001 â€” Final AI-Smeta-RU Architecture

## Status

Accepted for architecture refinement only.

## Context

The AI-Smeta-RU module needs a constrained architecture that supports draft
review workflows without implementing production business logic, persistence,
or final approvals.

## Decision

The module will be structured around the following layers:

- pi/ for entry points and schemas
- domain/ for pure domain models
- pipeline/ for staged workflow placeholders
- providers/ for interface isolation
- dapters/ for file-format and export integration
- services/ for orchestration placeholders
- eview/ for review gates and approval policy
- export/ for export structure placeholders
- estimator_package/ for the review package artifact

The MVP remains draft-only. GrandSmeta is the authoritative estimating environment,
and AI-Smeta-RU prepares an Estimator Package for review and handoff.

## Consequences

This refines the module into a clear architecture shell without implementing
real extraction, norm mapping, or Excel generation.
