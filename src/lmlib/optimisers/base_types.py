from typing import Union
from enum import Enum

class OptimisationType(Enum):
    MAXIMIZE = "maximize"
    MINIMIZE = "minimize"

class ConstraintType(Enum):
    EQUALITY = "="        # f(x) = 0
    INEQUALITY_NEQ = "!=" # f(x) ≠ 0
    INEQUALITY_LTE = "<=" # f(x) ≤ 0
    INEQUALITY_GTE = ">=" # f(x) ≥ 0
    INEQUALITY_LT = "<"   # f(x) < 0
    INEQUALITY_GT = ">"   # f(x) > 0

class ConstraintStrictness(Enum):
    HARD = "hard"  # Must
    SOFT = "soft"  # Preferred


DecisionVariable = Union[float, int, bool, str]