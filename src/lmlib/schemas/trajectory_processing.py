from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
from schemas.eta_calculation import LocationBase

# Base class for trajectory-related attributes
class TrajectoryBase(BaseModel):
    trajectory_id: str
    vessel_id: str  # MMSI number of the vessel
    name: str  # Name of the vessel
    destination_id: Optional[str] = None


# Common model for trajectory data
class TrajectoryDataBase(BaseModel):
    timestamp: datetime  # Timestamp from the AIS base station
    sog: Optional[float] = None  # Speed Over Ground (SOG)
    cog: Optional[float] = None  # Course Over Ground (COG)
    heading: Optional[float] = None  # Heading of the vessel
    navigational_status: Optional[str] = None  # Navigational status
    eta: Optional[datetime] = None


# Request Model for GET /v1/vessel/trajectories/ids
class TrajectoriesIdsRequest(BaseModel):
    limit: Optional[int] = 10


# Response Model for GET /v1/vessel/trajectories/ids
class TrajectoriesIdsResponse(BaseModel):
    ids: List[str]


# Request Model for GET /v1/vessel/trajectories/
class TrajectoriesRequest(BaseModel):
    limit: Optional[int] = 10


# Response Model for GET /v1/vessel/trajectories/
class TrajectoriesResponse(BaseModel):
    trajectories: List[str]


# Request Model for GET /v1/vessel/trajectories/{trajectory_id}
class TrajectoryDetailRequest(BaseModel):
    trajectory_id: str


# Response Model for GET /v1/vessel/trajectories/{trajectory_id}
class TrajectoryDetailResponse(TrajectoryBase, LocationBase, TrajectoryDataBase):
    pass


# Request Model for PUT /v1/vessel/trajectories/{trajectory_id}/segment
class TrajectorySegmentRequest(BaseModel):
    trajectory_id: str
    criteria: str = "duration"
    value: float


# Response Model for PUT /v1/vessel/trajectories/{trajectory_id}/segment
class TrajectorySegmentResponse(TrajectoryBase, LocationBase, TrajectoryDataBase):
    segment_id: str


# Request Model for GET /v1/vessel/trajectories/patterns/
class TrajectoryPatternsRequest(BaseModel):
    limit: Optional[int] = 10


# Response Model for GET /v1/vessel/trajectories/patterns/
class TrajectoryPatternsResponse(BaseModel):
    patterns: List[dict]
