from typing import Dict, Optional, Literal, ClassVar
from pydantic import BaseModel

class Area(BaseModel):
    """A representation of an Area."""
    model_id: ClassVar[Literal['dtmi:digitaltwins:isa95:Area;1']] = 'dtmi:digitaltwins:isa95:Area;1'

class Equipment(BaseModel):
    """A representation of Equipment."""
    model_id: ClassVar[Literal['dtmi:digitaltwins:isa95:Equipment;1']] = 'dtmi:digitaltwins:isa95:Equipment;1'

class EquipmentCapability(BaseModel):
    """A representation of Equipment Capability."""
    model_id: ClassVar[Literal['dtmi:digitaltwins:isa95:EquipmentCapability;1']] = 'dtmi:digitaltwins:isa95:EquipmentCapability;1'



    
class PhysicalAsset(BaseModel):
    """A representation of a Physical Asset."""
    model_id: ClassVar[Literal['dtmi:digitaltwins:isa95:PhysicalAsset;1']] = 'dtmi:digitaltwins:isa95:PhysicalAsset;1'

class OperationalLocation(BaseModel):
    """A representation of an Operational Location."""
    model_id: ClassVar[Literal['dtmi:digitaltwins:isa95:OperationalLocation;1']] = 'dtmi:digitaltwins:isa95:OperationalLocation;1'

class SpatialDefinition(BaseModel):
    """A representation of a Spatial Definition."""
    model_id: ClassVar[Literal['dtmi:digitaltwins:isa95:SpatialDefinition;1']] = 'dtmi:digitaltwins:isa95:SpatialDefinition;1'

    value: str
    format: str
    SRID: Optional[str] = None
    SRIDauthority: Optional[str] = None
    description: Optional[Dict] = None

class StorageZone(BaseModel):
    """A representation of a Storage Zone."""
    model_id: ClassVar[Literal['dtmi:digitaltwins:isa95:StorageZone;1']] = 'dtmi:digitaltwins:isa95:StorageZone;1'

class WorkflowSpecification(BaseModel):
    """A representation of a Workflow Specification."""
    model_id: ClassVar[Literal['dtmi:digitaltwins:isa95:WorkflowSpecification;1']] = 'dtmi:digitaltwins:isa95:WorkflowSpecification;1'

class WorkflowSpecificationNode(BaseModel):
    """A representation of a Workflow Specification Node."""
    model_id: ClassVar[Literal['dtmi:digitaltwins:isa95:WorkflowSpecificationNode;1']] = 'dtmi:digitaltwins:isa95:WorkflowSpecificationNode;1'

class WorkSchedule(BaseModel):
    """A representation of a Work Schedule."""
    model_id: ClassVar[Literal['dtmi:digitaltwins:isa95:WorkSchedule;1']] = 'dtmi:digitaltwins:isa95:WorkSchedule;1'

class EquipmentCapabilityProperty(BaseModel):
    model_id: ClassVar[Literal['dtmi:digitaltwins:isa95:EquipmentCapabilityProperty;1']] = 'dtmi:digitaltwins:isa95:EquipmentCapabilityProperty;1'

class ParameterSpecification(BaseModel):
    model_id: ClassVar[Literal['dtmi:digitaltwins:isa95:ParameterSpecification;1']] = 'dtmi:digitaltwins:isa95:ParameterSpecification;1'