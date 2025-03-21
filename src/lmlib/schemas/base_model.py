from typing import Dict

class Area:
    """A representation of an Area."""
    dt_id = "dtmi:digitaltwins:isa95:Area;1"

class Equipment:
    """A representation of Equipment."""
    dt_id = "dtmi:digitaltwins:isa95:Equipment;1"

class PhysicalAsset:
    """A representation of a Physical Asset."""
    dt_id = "dtmi:digitaltwins:isa95:PhysicalAsset;1"

class OperationalLocation:
    """A representation of an Operational Location."""
    dt_id = "dtmi:digitaltwins:isa95:OperationalLocation;1"

class SpatialDefinition:
    """A representation of a Spatial Definition."""
    dt_id = "dtmi:digitaltwins:isa95:SpatialDefinition;1"

    def __init__(self, 
                 value: str, 
                 format: str, 
                 SRID: str = None, 
                 SRIDauthority: str = None, 
                 description: Dict = None):
        self.value = value
        self.format = format
        self.SRID = SRID
        self.SRIDauthority = SRIDauthority
        self.description = description

class StorageZone:
    """A representation of a Storage Zone."""
    dt_id = "dtmi:digitaltwins:isa95:StorageZone;1"

class WorkflowSpecification:
    """A representation of a Workflow Specification."""
    dt_id = 'dtmi:digitaltwins:isa95:WorkflowSpecification;1'

class WorkflowSpecificationNode:
    """A representation of a Workflow Specification Node."""
    dt_id = "dtmi:digitaltwins:isa95:WorkflowSpecificationNode;1"

class WorkSchedule:
    """A representation of a Work Schedule."""
    dt_id = "dtmi:digitaltwins:isa95:WorkSchedule;1"
