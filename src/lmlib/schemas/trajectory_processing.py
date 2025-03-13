from abc import ABC, abstractmethod
from schemas.trajectory_processing import (
    TrajectoriesIdsRequest,
    TrajectoriesIdsResponse,
    TrajectoriesRequest,
    TrajectoriesResponse,
    TrajectoryDetailRequest,
    TrajectoryDetailResponse,
    TrajectorySegmentRequest,
    TrajectorySegmentResponse,
    TrajectoryPatternsRequest,
    TrajectoryPatternsResponse,
)

class TrajectoryProcessingService(ABC):
    
    @abstractmethod
    def get_trajectory_ids(self, request: TrajectoriesIdsRequest) -> TrajectoriesIdsResponse:
        """
        Fetch a list of trajectory IDs based on the provided request parameters.
        
        :param request: Contains the limit on the number of trajectory IDs to be returned.
        :return: A list of trajectory IDs.
        """
        pass

    @abstractmethod
    def get_trajectories(self, request: TrajectoriesRequest) -> TrajectoriesResponse:
        """
        Fetch a list of trajectory data based on the provided request parameters.
        
        :param request: Contains the limit on the number of trajectory data to be returned.
        :return: A list of trajectory data.
        """
        pass

    @abstractmethod
    def get_trajectory_detail(self, request: TrajectoryDetailRequest) -> TrajectoryDetailResponse:
        """
        Fetch detailed information for a specific trajectory using its ID.
        
        :param request: Contains the trajectory ID.
        :return: Detailed information about the trajectory.
        """
        pass

    @abstractmethod
    def update_trajectory_segment(self, request: TrajectorySegmentRequest) -> TrajectorySegmentResponse:
        """
        Update the trajectory segment based on provided criteria and value.
        
        :param request: Contains the trajectory ID, criteria, and threshold value for segmenting the trajectory.
        :return: Updated trajectory segment information.
        """
        pass

    @abstractmethod
    def get_trajectory_patterns(self, request: TrajectoryPatternsRequest) -> TrajectoryPatternsResponse:
        """
        Fetch trajectory patterns based on the provided request parameters.
        
        :param request: Contains the limit on the number of trajectory patterns to be returned.
        :return: A list of trajectory patterns.
        """
        pass
