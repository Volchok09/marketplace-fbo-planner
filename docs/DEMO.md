# Demo Walkthrough

The sample demo shows the public planning core without private seller data.

## Run

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -e .
fbo-planner plan \
  --rules examples/rules.sample.json \
  --run examples/run.sample.json \
  --out /tmp/fbo-plan.json
```

## Inputs

`examples/rules.sample.json` defines:

- product SKUs;
- product models;
- pack classes;
- reserve stock;
- available units;
- box capacity rules;
- marketplace adapter status.

`examples/run.sample.json` defines a weekly planning context:

- target planning window;
- max box count;
- marketplace demand signals;
- warehouse or cluster;
- FBO stock;
- inbound units;
- marketplace recommendation;
- days without stock.

## Output Shape

The planner returns:

- `items`: shipment rows by marketplace, warehouse, box, SKU, and quantity;
- `boxes`: box-level assignments and warnings;
- `production_shortfalls`: demand that cannot be covered from available units after reserves;
- `summary`: total units, boxes, and marketplace split.

Example summary:

```json
{
  "total_units": 67,
  "total_boxes": 10,
  "by_marketplace": {
    "Wildberries": 38,
    "Ozon": 29
  }
}
```

## Why This Demo Is Small

Real seller workflows contain private marketplace reports, spreadsheet IDs, stock data, prices, margins, and route constraints. The public demo keeps the shape of the workflow while using anonymized SKUs and simplified warehouses.

