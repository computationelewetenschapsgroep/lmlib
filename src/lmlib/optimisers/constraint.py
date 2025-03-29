from abc import ABC

from lmlib.optimisers.base_types import ConstraintType, ConstraintStrictness

class Constraint(ABC):
    def __init__(self, constraint_type: ConstraintType, strictness: ConstraintStrictness):
        """
        Base class for constraints.
        """
        self.constraint_type: ConstraintType = constraint_type
        self.strictness: ConstraintStrictness = strictness