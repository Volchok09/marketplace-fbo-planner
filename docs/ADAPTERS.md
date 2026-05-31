# Marketplace Adapters

Adapters convert marketplace-specific exports, API responses, or spreadsheet tabs into normalized demand signals.

The planning core should not know whether a row came from Wildberries, Ozon, Amazon FBA, eBay, AliExpress, or a seller's custom sheet.

## Normalized Demand Signal

```json
{
  "marketplace": "Ozon",
  "warehouse": "South Cluster",
  "sku": "ARM-RIO-4",
  "product_name": "Armrest for compact sedan",
  "daily_sales_units": 1.2,
  "fbo_stock_units": 1,
  "inbound_units": 0,
  "recommended_units": 15,
  "days_without_stock": 1
}
```

## Status

| Adapter | Status | Next step |
| --- | --- | --- |
| Wildberries | Prototype | Add XLSX importer and anonymized fixtures. |
| Ozon | Prototype | Add XLSX importer and cluster mapping tests. |
| Google Sheets | Planned | Add read/write helpers with sheet allowlists. |
| Amazon FBA | Roadmap | Map restock reports into demand signals. |
| eBay | Roadmap | Document fulfillment planning input formats. |
| AliExpress | Roadmap | Document cross-border replenishment inputs. |

## Adapter Rules

- Keep credentials and private reports out of the repository.
- Add anonymized fixtures for every parser.
- Normalize early and keep marketplace-specific logic out of the planning core.
- Prefer explicit mapping files over hidden assumptions.

