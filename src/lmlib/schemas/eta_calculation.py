from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import List
from utils import validate_wkt

# Base class to represent common attributes for location-based entities
class LocationBase(BaseModel):
    location: str  # WKT format for location

    @field_validator('location')
    def wkt_validator(cls, v):
        return validate_wkt(v) 

# Base class for vessel-specific attributes
class VesselBase(BaseModel):
    vessel_id: str  # MMSI number of the vessel
    destination_id: str


# Common base class for ETA estimates
class VesselETAEstimates(BaseModel):
    path: str
    sog: List[float]


# Request model for /v1/vessel/{vessel_id}/eta
class VesselETARequest(BaseModel):
    vessel_id: str


# Response model for /v1/vessel/{vessel_id}/eta
class VesselETAResponse(VesselBase, LocationBase):
    eta: datetime
    estimates: VesselETAEstimates


class MonopileETARequest(BaseModel):
    monopile_id: str


class MonopileETAResponse:
    planned_eta: datetime   
    estimated_eta: datetime
