from __future__ import annotations

import math
from collections import defaultdict
from typing import Any

from .models import BoxAssignment, BoxRule, DemandSignal, PlanResult, ProductRule, ShipmentItem


def _signals_from_run(run: dict[str, Any]) -> list[DemandSignal]:
    signals = []
    for row in run.get("demand_signals", []):
        signals.append(
            DemandSignal(
                marketplace=str(row["marketplace"]),
                warehouse=str(row["warehouse"]),
                sku=str(row["sku"]),
                product_name=str(row.get("product_name") or row["sku"]),
                daily_sales_units=float(row.get("daily_sales_units", 0)),
                fbo_stock_units=int(row.get("fbo_stock_units", 0)),
                inbound_units=int(row.get("inbound_units", 0)),
                recommended_units=(
                    int(row["recommended_units"])
                    if row.get("recommended_units") is not None
                    else None
                ),
                days_without_stock=int(row.get("days_without_stock", 0)),
            )
        )
    return signals


def _product_rules(rules: dict[str, Any]) -> dict[str, ProductRule]:
    result = {}
    for row in rules.get("products", []):
        result[str(row["sku"])] = ProductRule(
            sku=str(row["sku"]),
            model=str(row.get("model") or row["sku"]),
            pack_class=str(row.get("pack_class") or "standard"),
            reserve_units=int(row.get("reserve_units", 0)),
            available_units=(
                int(row["available_units"])
                if row.get("available_units") is not None
                else None
            ),
        )
    return result


def _box_rules(rules: dict[str, Any]) -> list[BoxRule]:
    result = []
    for row in rules.get("box_rules", []):
        result.append(
            BoxRule(
                name=str(row["name"]),
                pack_classes=tuple(row.get("pack_classes", [])),
                max_units=int(row["max_units"]),
                max_non_extra_units=(
                    int(row["max_non_extra_units"])
                    if row.get("max_non_extra_units") is not None
                    else None
                ),
                extra_pack_class=(
                    str(row["extra_pack_class"])
                    if row.get("extra_pack_class") is not None
                    else None
                ),
                max_extra_units=int(row.get("max_extra_units", 0)),
            )
        )
    return result


def _target_quantity(signal: DemandSignal, target_days: int) -> int:
    demand_target = math.ceil(signal.daily_sales_units * target_days)
    if signal.recommended_units is not None:
        demand_target = max(demand_target, signal.recommended_units)
    if signal.days_without_stock:
        demand_target += min(signal.days_without_stock, 7)
    return max(0, demand_target - signal.fbo_stock_units - signal.inbound_units)


def _score_signal(signal: DemandSignal, target_days: int) -> float:
    need = _target_quantity(signal, target_days)
    stockout_bonus = min(signal.days_without_stock, 14) * 3
    return need * 10 + signal.daily_sales_units * 5 + stockout_bonus


def _fits(box: BoxAssignment, item: ShipmentItem, rule: BoxRule) -> bool:
    if item.pack_class not in rule.pack_classes and item.pack_class != rule.extra_pack_class:
        return False
    if box.quantity + item.quantity > rule.max_units:
        return False
    if rule.extra_pack_class and rule.max_non_extra_units is not None:
        non_extra = sum(
            existing.quantity
            for existing in box.items
            if existing.pack_class != rule.extra_pack_class
        )
        extra = sum(
            existing.quantity
            for existing in box.items
            if existing.pack_class == rule.extra_pack_class
        )
        if item.pack_class == rule.extra_pack_class:
            return extra + item.quantity <= rule.max_extra_units
        return non_extra + item.quantity <= rule.max_non_extra_units
    return True


def _find_box_rule(product: ProductRule, rules: list[BoxRule]) -> BoxRule:
    for rule in rules:
        if product.pack_class in rule.pack_classes:
            return rule
    for rule in rules:
        if product.pack_class == rule.extra_pack_class:
            return rule
    raise ValueError(f"No box rule can pack SKU {product.sku} with class {product.pack_class}")


def build_plan(rules: dict[str, Any], run: dict[str, Any]) -> PlanResult:
    target_days = int(run.get("target_days", rules.get("target_days", 14)))
    max_boxes = int(run.get("max_boxes", rules.get("max_boxes", 20)))
    products = _product_rules(rules)
    box_rules = _box_rules(rules)
    warnings: list[str] = []
    production_shortfalls: dict[str, int] = defaultdict(int)
    remaining_available: dict[str, int | None] = {
        sku: (
            None
            if rule.available_units is None
            else max(0, rule.available_units - rule.reserve_units)
        )
        for sku, rule in products.items()
    }

    signals = sorted(
        _signals_from_run(run),
        key=lambda signal: _score_signal(signal, target_days),
        reverse=True,
    )

    boxes: list[BoxAssignment] = []
    items: list[ShipmentItem] = []
    next_box_by_destination: dict[tuple[str, str], int] = defaultdict(lambda: 1)

    for signal in signals:
        product = products.get(signal.sku)
        if not product:
            warnings.append(f"Missing product rule for SKU {signal.sku}; skipped.")
            continue

        target_qty = _target_quantity(signal, target_days)
        if target_qty <= 0:
            continue

        available = remaining_available.get(signal.sku)
        if available is not None:
            if available <= 0:
                production_shortfalls[signal.sku] += target_qty
                continue
            if target_qty > available:
                production_shortfalls[signal.sku] += target_qty - available
                target_qty = available

        rule = _find_box_rule(product, box_rules)
        quantity_left = target_qty
        while quantity_left > 0:
            if len(boxes) >= max_boxes:
                warnings.append(f"Max boxes reached at {max_boxes}; remaining demand was skipped.")
                return PlanResult(items, boxes, dict(production_shortfalls), warnings, metadata={"target_days": target_days})

            destination = (signal.marketplace, signal.warehouse)
            candidate = ShipmentItem(
                marketplace=signal.marketplace,
                warehouse=signal.warehouse,
                box=next_box_by_destination[destination],
                sku=signal.sku,
                product_name=signal.product_name,
                model=product.model,
                pack_class=product.pack_class,
                quantity=min(quantity_left, rule.max_units),
                reason=_reason(signal, target_days),
            )

            box = _last_compatible_box(boxes, candidate, rule)
            if box is None:
                box = BoxAssignment(
                    marketplace=signal.marketplace,
                    warehouse=signal.warehouse,
                    box=next_box_by_destination[destination],
                    rule_name=rule.name,
                )
                next_box_by_destination[destination] += 1
                boxes.append(box)

            while candidate.quantity > 0 and not _fits(box, candidate, rule):
                candidate.quantity -= 1
            if candidate.quantity <= 0:
                box.warnings.append(f"Could not fit SKU {signal.sku} into box rule {rule.name}.")
                break

            candidate.box = box.box
            box.items.append(candidate)
            items.append(candidate)
            quantity_left -= candidate.quantity
            if remaining_available.get(signal.sku) is not None:
                remaining_available[signal.sku] = max(0, int(remaining_available[signal.sku]) - candidate.quantity)

    return PlanResult(items, boxes, dict(production_shortfalls), warnings, metadata={"target_days": target_days})


def _last_compatible_box(
    boxes: list[BoxAssignment],
    item: ShipmentItem,
    rule: BoxRule,
) -> BoxAssignment | None:
    for box in reversed(boxes):
        if box.marketplace != item.marketplace or box.warehouse != item.warehouse:
            continue
        if box.rule_name != rule.name:
            continue
        if _fits(box, item, rule):
            return box
    return None


def _reason(signal: DemandSignal, target_days: int) -> str:
    target = _target_quantity(signal, target_days)
    parts = [f"target {target_days}d demand requires {target} units"]
    if signal.recommended_units is not None:
        parts.append(f"marketplace recommendation {signal.recommended_units}")
    if signal.days_without_stock:
        parts.append(f"{signal.days_without_stock} days without stock")
    return "; ".join(parts)
