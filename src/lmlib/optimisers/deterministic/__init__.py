from abc import ABC, abstractmethod
from typing import Any

class DeterministicState:
    """Represents a generic state in a deterministic system."""
    
    def __init__(self, name: str, attributes: dict[str, Any]):
        self.name = name
        self.attributes = attributes  
        
class DeterministicTransitions(ABC):
    """Abstract base class for deterministic transition models."""

    @abstractmethod
    def next_state(self, current_state: DeterministicState) -> DeterministicState:
        """Determine the next state in the system."""
        pass