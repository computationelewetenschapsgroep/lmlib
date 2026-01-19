from typing import Tuple
from lmlib.optimisers.deterministic import DeterministicState


class RouteState(DeterministicState):
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

class VehicleState(DeterministicState):
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
