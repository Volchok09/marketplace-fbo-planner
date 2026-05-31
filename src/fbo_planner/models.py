from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class DemandSignal:
    marketplace: str
    warehouse: str
    sku: str
    product_name: str
    daily_sales_units: float
    fbo_stock_units: int
    inbound_units: int = 0
    recommended_units: int | None = None
    days_without_stock: int = 0


@dataclass(frozen=True)
class ProductRule:
    sku: str
    model: str
    pack_class: str
    reserve_units: int = 0
    available_units: int | None = None


@dataclass(frozen=True)
class BoxRule:
    name: str
    pack_classes: tuple[str, ...]
    max_units: int
    max_non_extra_units: int | None = None
    extra_pack_class: str | None = None
    max_extra_units: int = 0


@dataclass
class ShipmentItem:
    marketplace: str
    warehouse: str
    box: int
    sku: str
    product_name: str
    model: str
    pack_class: str
    quantity: int
    reason: str


@dataclass
class BoxAssignment:
    marketplace: str
    warehouse: str
    box: int
    rule_name: str
    items: list[ShipmentItem] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def quantity(self) -> int:
        return sum(item.quantity for item in self.items)


@dataclass
class PlanResult:
    items: list[ShipmentItem]
    boxes: list[BoxAssignment]
    production_shortfalls: dict[str, int]
    warnings: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "metadata": self.metadata,
            "items": [item.__dict__ for item in self.items],
            "boxes": [
                {
                    "marketplace": box.marketplace,
                    "warehouse": box.warehouse,
                    "box": box.box,
                    "rule_name": box.rule_name,
                    "quantity": box.quantity,
                    "warnings": box.warnings,
                    "items": [item.__dict__ for item in box.items],
                }
                for box in self.boxes
            ],
            "production_shortfalls": self.production_shortfalls,
            "warnings": self.warnings,
            "summary": self.summary(),
        }

    def summary(self) -> dict[str, Any]:
        by_marketplace: dict[str, int] = {}
        by_warehouse: dict[str, int] = {}
        for item in self.items:
            by_marketplace[item.marketplace] = by_marketplace.get(item.marketplace, 0) + item.quantity
            key = f"{item.marketplace}:{item.warehouse}"
            by_warehouse[key] = by_warehouse.get(key, 0) + item.quantity
        return {
            "total_units": sum(item.quantity for item in self.items),
            "total_boxes": len(self.boxes),
            "by_marketplace": by_marketplace,
            "by_warehouse": by_warehouse,
        }

