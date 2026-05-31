from __future__ import annotations

from typing import Protocol

from fbo_planner.models import DemandSignal


class MarketplaceAdapter(Protocol):
    name: str

    def read_demand_signals(self) -> list[DemandSignal]:
        """Return normalized demand signals for the planning core."""

