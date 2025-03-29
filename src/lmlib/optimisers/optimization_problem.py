from typing import Callable, List, Optional, Any

from lmlib.optimisers.base_types import DecisionVariable, OptimisationType
from lmlib.optimisers.constraint import Constraint

class OptimizationProblem:
    """
    General optimization problem model.
    """
    def __init__(
        self, 
        optimisation_type: OptimisationType, 
        objective_function: Callable[..., Any],
        constraints: Optional[List[Constraint]],
        decision_variables: list[DecisionVariable]
    ):
        self.optimisation_type = optimisation_type
        self.objective_function = objective_function
        self.constraints = constraints
        self.decision_variables = decision_variables