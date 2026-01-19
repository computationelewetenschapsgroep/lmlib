from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from enum import Enum

from schemas.eta_calculation import LocationBase


# Enum for the status of the _ based on one of predefined activity types
class StatusEnum(str, Enum):
    ACTIVE = 'ACTIVE'
    INACTIVE = 'INACTIVE'

# Enum for the role of the _ based on one of the predefined roles
class RoleEnum(str, Enum):
    VESSEL = 'VESSEL'
    MONOPILE = 'MONOPILE'
    PORT = 'PORT'

# Common base class for assets like Vessel, Monopile, and Port
class AssetBase(BaseModel, LocationBase):
    twin_id: str
    status: StatusEnum
    role: RoleEnum
    properties: Dict[str, Any]  # JSON

class Vessel(AssetBase):
    vessel_id: str #MMSI number of the vesse


class Monopile(AssetBase):
    monopile_id: str


class Port(AssetBase):
    port_id: str


# Request model for GET /v1/at/vessels/{vessel_id}
class VesselGetRequest(BaseModel):
    vessel_id: str


# Response model for GET /v1/at/vessels/{vessel_id}
class VesselGetResponse(Vessel):
    pass


# Request model for PUT /v1/at/vessels/{vessel_id}
class VesselPutRequest(BaseModel, LocationBase):
    vessel_id: str
    name: str
    responsibility: RoleEnum


# Response model for PUT /v1/at/vessels/{vessel_id}
class VesselPutResponse(BaseModel):
    twin_id: str


# Request model for DELETE /v1/at/vessels/{vessel_id}
class VesselDeleteRequest(BaseModel):
    vessel_id: str


# Response model for DELETE /v1/at/vessels/{vessel_id}
class VesselDeleteResponse(BaseModel):
    twin_id: str


# Request model for GET /v1/at/vessels/
class VesselGetListRequest(BaseModel):
    limit: Optional[int] = 10


# Response model for GET /v1/at/vessels/
class VesselGetListResponse(BaseModel):
    vessels: List[Vessel]


# Request model for GET /v1/at/monopiles/{monopile_id}
class MonopileGetRequest(BaseModel):
    monopile_id: str


# Response model for GET /v1/at/monopiles/{monopile_id}
class MonopileGetResponse(Monopile):
    pass


# Request model for PUT /v1/at/monopiles/{monopile_id}
class MonopilePutRequest(BaseModel, LocationBase):
    monopile_id: str
    status: StatusEnum


# Response model for PUT /v1/at/monopiles/{monopile_id}
class MonopilePutResponse(BaseModel):
    twin_id: str


# Request model for DELETE /v1/at/monopiles/{monopile_id}
class MonopileDeleteRequest(BaseModel):
    monopile_id: str


# Response model for DELETE /v1/at/monopiles/{monopile_id}
class MonopileDeleteResponse(BaseModel):
    twin_id: str


# Request model for GET /v1/at/monopiles/
class MonopileGetListRequest(BaseModel):
    limit: Optional[int] = 10


# Response model for GET /v1/at/monopiles/
class MonopileGetListResponse(BaseModel):
    monopiles: List[Monopile]


# Request model for PUT /v1/at/connect/
class ConnectionPutRequest(BaseModel):
    source_twin_id: str
    relationship_name: str
    target_twin_id: str


# Response model for PUT /v1/at/connect/
class ConnectionPutResponse(BaseModel):
    twin_id: str


# Request model for GET /v1/at/relations/{twin_id}
class RelationGetRequest(BaseModel):
    twin_id: str
    limit: Optional[int] = 10


# Response model for GET /v1/at/relations/{twin_id}
class RelationGetResponse(BaseModel):
    relations: List[Dict[str, Any]]


# Request model for DELETE /v1/at/relations/{relation_id}
class RelationDeleteRequest(BaseModel):
    relation_id: str


# Request model for GET /v1/at/ports/{port_id}
class PortGetRequest(BaseModel):
    port_id: str


# Response model for GET /v1/at/ports/{port_id}
class PortGetResponse(Port):
    pass


# Request model for PUT /v1/at/ports/{port_id}
class PortPutRequest(BaseModel, LocationBase):
    port_id: str
    name: str


# Response model for PUT /v1/at/ports/{port_id}
class PortPutResponse(BaseModel):
    twin_id: str


# Request model for DELETE /v1/at/ports/{port_id}
class PortDeleteRequest(BaseModel):
    port_id: str


# Response model for DELETE /v1/at/ports/{port_id}
class PortDeleteResponse(BaseModel):
    twin_id: str


# Request model for GET /v1/at/ports/
class PortGetListRequest(BaseModel):
    limit: Optional[int] = 10


# Response model for GET /v1/at/ports/
class PortGetListResponse(BaseModel):
    ports: List[Port]
