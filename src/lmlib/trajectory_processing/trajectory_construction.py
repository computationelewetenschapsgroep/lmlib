from abc import ABC, abstractmethod
from schemas.trajectory_construction import VesselProbeRequest

class TrajectoryProcessingService(ABC):
    
    @abstractmethod
    def get_trajectory_ids(self, request: VesselProbeRequest):
        pass