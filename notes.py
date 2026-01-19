

class EqualityConstraint(Constraint):
    def __init__(self, function: Callable[[float], float], strictness: ConstraintStrictness = ConstraintStrictness.HARD):
        """
        Represents an equality constraint: f(x) = 0.

        :param function: A function that should be equal to zero.
        :param strictness: Whether the constraint is hard or soft.
        """
        super().__init__(ConstraintType.EQUALITY, strictness)
        self.function: Callable[[float], float] = function

    def is_satisfied(self, x: float) -> bool:
        return abs(self.function(x)) == 0  


class InequalityConstraint(Constraint):
    def __init__(self, function: Callable[[float], float], strictness: ConstraintStrictness = ConstraintStrictness.HARD):
        """
        Represents an inequality constraint: f(x) ≤ 0.
        """
        super().__init__(ConstraintType.INEQUALITY, strictness)
        self.function: Callable[[float], float] = function

    def is_satisfied(self, x: float) -> bool:
        return self.function(x) <= 0


class IntegerConstraint(Constraint):
    def __init__(self, strictness: ConstraintStrictness = ConstraintStrictness.HARD):
        """
        Represents an integer constraint: x ∈ ℤ (x must be an integer).
        """
        super().__init__(ConstraintType.INTEGER, strictness)

    def is_satisfied(self, x: float) -> bool:
        return x.is_integer()


# 7. Feasibility Check Function
def is_feasible(x: float, constraints: list[Constraint]) -> bool:
    """
    Checks if a given value x is feasible (satisfies all hard constraints).

    :param x: The decision variable value
    :param constraints: List of constraints to check
    :return: True if x satisfies all hard constraints, False otherwise
    """
    for constraint in constraints:
        if constraint.strictness == ConstraintStrictness.HARD and not constraint.is_satisfied(x):
            return False
    return True



equality_constraint = EqualityConstraint(lambda x: x - 5)
constraints = [equality_constraint]
x = 5.0 
print(f"equality_constraint : x feasible: {is_feasible(x, constraints)}")
