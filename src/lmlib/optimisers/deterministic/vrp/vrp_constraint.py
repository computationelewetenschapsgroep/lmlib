from typing import Optional

from lmlib.optimisers.base_types import ConstraintStrictness, ConstraintType
from lmlib.optimisers.constraint import Constraint

class VRPConstraint(Constraint):
    """Represents constraints specific to the Vehicle Routing Problem."""
    
    def __init__(
        self, 
        property_name: str, 
        constraint_type: ConstraintType,
        min_value: Optional[float], 
        max_value: Optional[float], 
        strictness: ConstraintStrictness = ConstraintStrictness.HARD
    ):
        super().__init__(constraint_type, strictness)
        self.property_name = property_name
        self.min_value = min_value
        self.max_value = max_value