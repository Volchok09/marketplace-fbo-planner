# Architecture

Marketplace FBO Planner is split into four layers:

1. Data adapters.
2. Planning core.
3. Operator interface.
4. AI-assisted review and maintenance.

## 1. Data Adapters

Adapters convert marketplace-specific exports or API responses into generic demand signals:

```json
{
  "marketplace": "Ozon",
  "warehouse": "South Cluster",
  "sku": "ARM-RIO-4",
  "daily_sales_units": 1.2,
  "fbo_stock_units": 1,
  "inbound_units": 0,
  "recommended_units": 15,
  "days_without_stock": 1
}
```

Current public status:

- Wildberries: prototype shape based on internal workflow.
- Ozon: prototype shape based on internal workflow.
- Amazon FBA: roadmap.
- eBay fulfillment: roadmap.
- AliExpress / cross-border fulfillment: roadmap.

## 2. Planning Core

The core is marketplace-agnostic. It uses:

- demand signals;
- product pack classes;
- available production stock;
- reserve stock;
- box capacity rules;
- weekly target days;
- max box limits.

The core produces:

- shipment items;
- box assignments;
- production shortfalls;
- warnings;
- summary tables.

## 3. Operator Interface

The original production workflow uses Google Sheets as the operator surface:

- source tabs hold stock, production, box rules, and transport routes;
- final tabs show the shipment plan;
- technical tabs map visual cells to machine-readable plan rows;
- Apps Script lets the operator adjust quantities while preserving validation.

The public repository does not contain private spreadsheet IDs or credentials. A reusable template is planned.

## 4. AI-Assisted Review

AI is useful because weekly FBO planning contains both stable rules and changing exceptions:

- marketplace warehouse availability changes;
- recommendations can conflict with stock or production constraints;
- some routes become unavailable for a week;
- human notes are often spoken or written informally;
- shipment tradeoffs need short explanations.

The intended AI workflow:

1. Read the weekly run context.
2. Check missing inputs.
3. Generate or review the plan.
4. Explain tradeoffs to the operator.
5. Convert repeated corrections into stable rules.

This keeps the deterministic core small while still supporting real-world messy operations.

