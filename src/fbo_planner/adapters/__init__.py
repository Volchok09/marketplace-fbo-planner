"""Marketplace adapter boundaries.

Adapters translate marketplace exports or APIs into the generic demand signal
shape consumed by the planning core.
"""

from .registry import ADAPTER_STATUS

__all__ = ["ADAPTER_STATUS"]

