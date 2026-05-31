# Roadmap

Marketplace FBO Planner is intentionally small today. The goal is to grow from a working planning core into a practical replenishment workflow for independent marketplace sellers.

## v0.1 Public Alpha

Status: shipped.

- Generic planning data model.
- JSON rules and weekly run input.
- CLI plan generation.
- Anonymized sample data.
- Box assignment validation.
- Public docs for the spreadsheet-plus-AI workflow.

## v0.2 Operator Spreadsheet Workflow

Goal: make the workflow useful for sellers who live in Google Sheets.

- Google Sheets template with sample tabs.
- Safe sync helper with explicit output sheet allowlists.
- Technical plan-data tab for manual edits.
- Spreadsheet-ready summary tables.
- Screenshots and walkthrough docs.

## v0.3 Marketplace Importers

Goal: reduce manual data shaping.

- Wildberries CSV/XLSX importer.
- Ozon CSV/XLSX importer.
- Shared normalization tests.
- Warehouse and cluster mapping files.
- Fixture policy for anonymized seller exports.

## v0.4 Global Adapter Layer

Goal: prove that the planning core can work beyond the original Russian marketplace workflow.

- Amazon FBA restock report adapter.
- eBay fulfillment planning adapter notes.
- AliExpress and cross-border replenishment adapter notes.
- Configurable region and route packs.

## v0.5 AI-Assisted Maintenance

Goal: make the messy weekly exception loop easier to maintain.

- Prompt templates for plan review.
- Rule-change extraction from operator feedback.
- Pull request checklist for adapter changes.
- Regression tests for stockout, box-capacity, and route-coverage scenarios.
- Human-readable tradeoff explanations in plan output.

## Open Questions

- How much planning logic belongs in deterministic code versus AI-assisted review?
- What is the smallest spreadsheet template that still feels useful to a real seller?
- How should route costs and non-local logistics fees be represented without overfitting to one marketplace?
- What anonymized fixture format makes it easy for contributors to add importers safely?

