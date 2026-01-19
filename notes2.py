from abc import ABC, abstractmethod
from typing import Callable, List, Optional, Any, Union,Tuple
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
    HARD = "hard"  # Must be satisfied
    SOFT = "soft"  # Preferred but not required


DecisionVariable = Union[float, int, bool, str]


class Constraint(ABC):
    def __init__(self, constraint_type: ConstraintType, strictness: ConstraintStrictness):
        """
        Base class for constraints.
        """
        self.constraint_type: ConstraintType = constraint_type
        self.strictness: ConstraintStrictness = strictness

class OptimizationProblem:
    """
    General optimization problem model.
    """
    def __init__(
        self, 
        opt_type: OptimisationType, 
        objective_function: Callable[..., Any],
        constraints: Optional[List[Constraint]],
        decision_variables: list[DecisionVariable]
    ):
        self.opt_type = opt_type
        self.objective_function = objective_function
        self.constraints = constraints
        self.decision_variables = decision_variables


class State:
    """Represents a generic state in a deterministic system."""
    
    def __init__(self, name: str, attributes: dict[str, Any]):
        self.name = name
        self.attributes = attributes  
        
class DeterministicTransitions(ABC):
    """Abstract base class for deterministic transition models."""

    @abstractmethod
    def next_state(self, current_state: State) -> State:
        """Determine the next state in the system."""
        pass


class RouteState(State):
    """Represents a vehicle's location and time in a routing problem."""
    
    def __init__(
        self, 
        location: str, 
        arrival_time: float, 
        time_window: Tuple[float, float]
    ):

        super().__init__(
            name=location, 
            attributes={
                "arrival_time": arrival_time, 
                "time_window": time_window
            }
        )

class VehicleState(State):
    """Represents the state of a vehicle in a VRP."""
    
    def __init__(
        self, 
        vehicle_id: str, 
        location: str, 
        available_capacity: float, 
        current_time: float
    ):
        super().__init__(
            vehicle_id=vehicle_id, 
            attributes={
                "location": location,
                "available_capacity": available_capacity,
                "current_time": current_time
            }
        )


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

class VRP(OptimizationProblem, DeterministicTransitions):
    def __init__(
        self,
        vehicles: List[VehicleState],  
        locations: List[RouteState],  
        constraints: List[VRPConstraint],  
        objective_function: Callable[..., float],  
        decision_variables: List[float],  
        optimisation_type: OptimisationType = OptimisationType.MINIMIZE
    ):
        OptimizationProblem.__init__(
            self, 
            optimisation_type, 
            objective_function, 
            decision_variables, 
            constraints
        )
        self.vehicles = vehicles
        self.locations = locations


# https://web.stanford.edu/group/sisl/k12/optimization/MO-unit3-pdfs/3.1introandgraphical.pdf
# https://en.wikipedia.org/wiki/Constraint_(mathematics)#Hard_and_soft_constraints
# https://en.wikipedia.org/wiki/Constrained_optimization


# Deterministic optimization problem
# - all inputs and constraints are known and fixed (no randomness).
# - goal is to find best values for decision variables that optimize the objective function while satisfying constraints.


# https://en.wikipedia.org/wiki/Deterministic_finite_automaton

# Deterministic Transitions 
#  - system follows fixed rules for evolving from one state to another
#  - example = VRP => truck moves from one location to another