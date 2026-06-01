import json
import unittest
from pathlib import Path

from fbo_planner import build_plan


ROOT = Path(__file__).resolve().parents[1]


def load_json(name: str) -> dict:
    return json.loads((ROOT / "examples" / name).read_text(encoding="utf-8"))


class PlannerTest(unittest.TestCase):
    def test_sample_plan_generates_items_and_boxes(self) -> None:
        plan = build_plan(load_json("rules.sample.json"), load_json("run.sample.json"))

        self.assertTrue(plan.items)
        self.assertTrue(plan.boxes)
        self.assertGreater(plan.summary()["total_units"], 0)
        self.assertLessEqual(plan.summary()["total_boxes"], 12)

    def test_box_quantities_do_not_exceed_rule_max(self) -> None:
        rules = load_json("rules.sample.json")
        plan = build_plan(rules, load_json("run.sample.json"))
        max_by_rule = {rule["name"]: rule["max_units"] for rule in rules["box_rules"]}

        for box in plan.boxes:
            self.assertLessEqual(box.quantity, max_by_rule[box.rule_name])

    def test_records_production_shortfall_when_available_units_are_not_enough(self) -> None:
        rules = load_json("rules.sample.json")
        run = load_json("run.sample.json")
        for product in rules["products"]:
            if product["sku"] == "ARM-RIO-4":
                product["available_units"] = 8
                product["reserve_units"] = 2

        plan = build_plan(rules, run)

        self.assertIn("ARM-RIO-4", plan.production_shortfalls)
        self.assertGreater(plan.production_shortfalls["ARM-RIO-4"], 0)


if __name__ == "__main__":
    unittest.main()
