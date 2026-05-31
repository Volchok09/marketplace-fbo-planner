from __future__ import annotations

import argparse
import json
from pathlib import Path

from .planner import build_plan


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def command_plan(args: argparse.Namespace) -> None:
    rules = load_json(args.rules)
    run = load_json(args.run)
    plan = build_plan(rules, run).to_dict()
    text = json.dumps(plan, ensure_ascii=False, indent=2)
    if args.out:
        args.out.write_text(text + "\n", encoding="utf-8")
    print(text)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Marketplace FBO planning helper.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    plan = subparsers.add_parser("plan", help="Build a shipment plan from JSON rules and run input.")
    plan.add_argument("--rules", type=Path, required=True)
    plan.add_argument("--run", type=Path, required=True)
    plan.add_argument("--out", type=Path)
    plan.set_defaults(func=command_plan)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()

