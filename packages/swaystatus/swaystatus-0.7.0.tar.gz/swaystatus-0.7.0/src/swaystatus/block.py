"""A block represents a unit of content for the status bar."""

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(slots=True, kw_only=True)
class Block:
    """
    Data class that maps directly on to the JSON representation.

    See the "BODY" section of swaybar-protocol(7) for a full description.
    """

    full_text: str | None = None
    short_text: str | None = None
    color: str | None = None
    background: str | None = None
    border: str | None = None
    border_top: int | None = None
    border_bottom: int | None = None
    border_left: int | None = None
    border_right: int | None = None
    min_width: int | str | None = None
    align: str | None = None
    name: str | None = None
    instance: str | None = None
    urgent: bool | None = None
    separator: bool | None = None
    separator_block_width: int | None = None
    markup: str | None = None

    def dict(self) -> dict[str, Any]:
        """Return a dict representation of this instance."""
        return {name: value for name, value in asdict(self).items() if value is not None}
