from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path

from dataclasses import dataclass


# Frozen=True creates an implicit hash method, eq is created by default
@dataclass(frozen=True)
class BootstrapPathsDTO:
    log_dir: Path
    steam_ids: list[int]
