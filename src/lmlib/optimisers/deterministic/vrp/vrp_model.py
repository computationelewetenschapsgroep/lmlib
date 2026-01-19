from typing import Callable, List

from lmlib.optimisers.deterministic import DeterministicTransitions
from lmlib.optimisers.optimization_problem import OptimizationProblem
from lmlib.optimisers.base_types import OptimisationType
from lmlib.optimisers.deterministic.vrp.vrp_constraint import VRPConstraint
from lmlib.optimisers.deterministic.vrp.vrp_state import RouteState, VehicleState


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