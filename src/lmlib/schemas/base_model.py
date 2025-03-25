from typing import Dict, Optional
from pydantic import BaseModel, Field

class Area(BaseModel):
    """A representation of an Area."""
    model_id: str = Field("dtmi:digitaltwins:isa95:Area;1", const=True)

class Equipment(BaseModel):
    """A representation of Equipment."""
    model_id: str = Field("dtmi:digitaltwins:isa95:Equipment;1", const=True)

class PhysicalAsset(BaseModel):
    """A representation of a Physical Asset."""
    model_id: str = Field("dtmi:digitaltwins:isa95:PhysicalAsset;1", const=True)

class OperationalLocation(BaseModel):
    """A representation of an Operational Location."""
    model_id: str = Field("dtmi:digitaltwins:isa95:OperationalLocation;1", const=True)

class SpatialDefinition(BaseModel):
    """A representation of a Spatial Definition."""
    model_id: str = Field("dtmi:digitaltwins:isa95:SpatialDefinition;1", const=True)

    value: str
    format: str
    SRID: Optional[str] = None
    SRIDauthority: Optional[str] = None
    description: Optional[Dict] = None

class StorageZone(BaseModel):
    """A representation of a Storage Zone."""
    model_id: str = Field("dtmi:digitaltwins:isa95:StorageZone;1", const=True)

class WorkflowSpecification(BaseModel):
    """A representation of a Workflow Specification."""
    model_id: str = 'dtmi:digitaltwins:isa95:WorkflowSpecification;1'

class WorkflowSpecificationNode(BaseModel):
    """A representation of a Workflow Specification Node."""
    model_id: str = Field("dtmi:digitaltwins:isa95:WorkflowSpecificationNode;1", const=True)

class WorkSchedule(BaseModel):
    """A representation of a Work Schedule."""
    model_id: str = Field("dtmi:digitaltwins:isa95:WorkSchedule;1", const=True)
