import gc
from dataclasses import dataclass
from typing import Dict, Generator

import pytest


@dataclass
class _State:
    was_enabled: bool
    did_gc: bool = False

    def collect_cb(self, phase: str, info: Dict[str, int]) -> None:
        self.did_gc = True


@pytest.fixture
def nogarbage() -> Generator[None, None, None]:
    state = _State(
        was_enabled=gc.isenabled(),
    )

    gc.disable()
    gc.freeze()
    try:
        gc.callbacks.append(state.collect_cb)
        yield
        gc.callbacks.remove(state.collect_cb)
        assert not state.did_gc, "Garbage collected during test"
        for gen in range(3):
            assert gc.collect(gen) == 0, "Garbage collected after test"
    finally:
        gc.unfreeze()
        if state.was_enabled:
            gc.enable()
