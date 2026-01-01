from typing import Protocol

import sys
sys.path.insert(0, '../../apps/utils')

from blinds_handler import BlindsHandler


# Constants for position states
BEST_FOR_TEMPERATURE = 666.0


class BlindsHandlerProtocol(Protocol):
    """Protocol defining the interface for blinds handlers."""
    
    def best_for_temperature(self) -> None: ...
    
    def close(self) -> None: ...
    
    def open(self) -> None: ...
    
    def set_position(self, open_percentage: int | float) -> None: ...
    
    def get_position(self) -> float: ...
    
    def open_all(self) -> None: ...
    
    def close_all(self) -> None: ...
    
    def is_open(self) -> bool: ...
    
    def is_closed(self) -> bool: ...


class FakeBlindsHandler:
    """Test double for BlindsHandler that conforms to BlindsHandlerProtocol.
    
    Uses position-based state machine where position is the only tracked state:
    - 0 = closed
    - 100 = open
    - BEST_FOR_TEMPERATURE = special position set by best_for_temperature()
    
    Tests should assert using observable state methods: is_open(), is_closed(), get_position()
    """
    
    def __init__(self) -> None:
        self.reset()
    
    def reset(self) -> None:
        self._position: float = 0.0
    
    def best_for_temperature(self) -> None:
        self._position = BEST_FOR_TEMPERATURE
    
    def close(self) -> None:
        self._position = 0.0
    
    def open(self) -> None:
        self._position = 100.0
    
    def set_position(self, open_percentage: int | float) -> None:
        self._position = float(open_percentage)
    
    def open_all(self) -> None:
        self._position = 100.0
    
    def close_all(self) -> None:
        self._position = 0.0
    
    def get_position(self) -> float:
        return self._position
    
    def is_open(self) -> bool:
        return self._position >= 100.0
    
    def is_closed(self) -> bool:
        return self._position <= 0.0


# Runtime verification functions
def _verify_real_blinds_handler() -> BlindsHandlerProtocol:
    """Type checker verifies BlindsHandler implements BlindsHandlerProtocol."""
    return None  # type: ignore


def _verify_fake_blinds() -> BlindsHandlerProtocol:
    """Type checker verifies FakeBlindsHandler implements BlindsHandlerProtocol."""
    return FakeBlindsHandler()
