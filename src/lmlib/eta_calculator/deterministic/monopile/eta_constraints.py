from typing import Optional

from lmlib.optimisers.base_types import ConstraintStrictness, ConstraintType
from lmlib.optimisers.constraint import Constraint

class ETAConstraints(Constraint):
    """Represents constraints specific to the Vehicle Routing Problem."""
    
    def __init__(
        self, 
        #property_name: str, 
        constraint_type: ConstraintType,
        # min_value: Optional[float], 
        # max_value: Optional[float], 
        strictness: ConstraintStrictness = ConstraintStrictness.HARD
    ):
        super().__init__(constraint_type, strictness)

    def __call__(self):
        return 


