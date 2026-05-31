from __future__ import annotations

import csv
from pathlib import Path

from fbo_planner.models import DemandSignal


def read_sample_csv(path: Path) -> list[DemandSignal]:
    """Read a normalized Ozon-style CSV export."""
    with path.open("r", encoding="utf-8", newline="") as handle:
        rows = csv.DictReader(handle)
        return [
            DemandSignal(
                marketplace="Ozon",
                warehouse=row["warehouse"],
                sku=row["sku"],
                product_name=row["product_name"],
                daily_sales_units=float(row["daily_sales_units"]),
                fbo_stock_units=int(row["fbo_stock_units"]),
                inbound_units=int(row.get("inbound_units") or 0),
                recommended_units=(
                    int(row["recommended_units"])
                    if row.get("recommended_units")
                    else None
                ),
                days_without_stock=int(row.get("days_without_stock") or 0),
            )
            for row in rows
        ]

