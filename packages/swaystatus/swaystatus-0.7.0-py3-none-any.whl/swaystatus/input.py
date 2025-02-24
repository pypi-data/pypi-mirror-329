import json
from functools import cached_property
from typing import IO, Iterable, Iterator

from .click_event import ClickEvent
from .element import BaseElement

type Key = tuple[str, str | None]


class InputDelegator:
    """Handle click events, sending them to the appropriate element's handler."""

    def __init__(self, elements: Iterable[BaseElement]) -> None:
        self.elements = list(elements)

    @cached_property
    def elements_by_key(self) -> dict[Key, BaseElement]:
        return {(e.name, e.instance): e for e in self.elements}

    def process(self, file: IO[str]) -> Iterator[ClickEvent]:
        assert file.readline().strip() == "["
        for line in file:
            event = ClickEvent(**json.loads(line.strip().lstrip(",")))
            if event.name:
                try:
                    element = self.elements_by_key[(event.name, event.instance)]
                except KeyError:
                    element = self.elements_by_key[(event.name, None)]
                element.on_click(event)
                yield event
