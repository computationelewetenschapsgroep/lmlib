from typing import Callable, List, Optional, Any
from lmlib.optimisers.constraint import Constraint
from lmlib.optimisers.base_types import DecisionVariable, OptimisationType, ConstraintStrictness, ConstraintType

class OptimizationProblem:
    def __init__(
        self, 
        optimisation_type: OptimisationType, 
        objective_function: Callable[..., Any],
        constraints: Optional[List[Constraint]],
        decision_variables: List[DecisionVariable]
    ):
        self.optimisation_type = optimisation_type
        self.objective_function = objective_function
        self.constraints = constraints
        self.decision_variables = decision_variables



def test_optimisation_type():
    assert OptimisationType.MAXIMIZE.value == "maximize"
    assert OptimisationType.MINIMIZE.value == "minimize"

def test_constraint_type():
    assert ConstraintType.EQUALITY.value == "="
    assert ConstraintType.INEQUALITY_NEQ.value == "!="
    assert ConstraintType.INEQUALITY_LTE.value == "<="
    assert ConstraintType.INEQUALITY_GTE.value == ">="
    assert ConstraintType.INEQUALITY_LT.value == "<"
    assert ConstraintType.INEQUALITY_GT.value == ">"

def test_constraint_strictness():
    assert ConstraintStrictness.HARD.value == "hard"
    assert ConstraintStrictness.SOFT.value == "soft"

def test_constraint():
    constraint = Constraint(ConstraintType.EQUALITY, ConstraintStrictness.HARD)
    assert constraint.constraint_type == ConstraintType.EQUALITY
    assert constraint.strictness == ConstraintStrictness.HARD

def test_optimization_problem():
    def mock_objective_function(x, y):
        return x + y

    constraint = Constraint(ConstraintType.INEQUALITY_LTE, ConstraintStrictness.SOFT)

    problem = OptimizationProblem(
        OptimisationType.MAXIMIZE,
        mock_objective_function,
        [constraint],
        [1.0, 2.0]
    )

    assert problem.optimisation_type == OptimisationType.MAXIMIZE
    assert problem.objective_function(1, 2) == 3  # 1 + 2 = 3
    assert len(problem.constraints) == 1
    assert problem.constraints[0].constraint_type == ConstraintType.INEQUALITY_LTE
    assert problem.constraints[0].strictness == ConstraintStrictness.SOFT
    assert problem.decision_variables == [1.0, 2.0]
