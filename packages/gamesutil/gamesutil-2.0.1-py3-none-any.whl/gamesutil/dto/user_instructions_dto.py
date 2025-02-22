from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path

    from gamesutil.enums.user_request import UserRequest


# Frozen=True creates an implicit hash method, eq is created by default
@dataclass(frozen=True)
class UserInstructionsDTO:
    request: UserRequest
    save_manifest: Path
