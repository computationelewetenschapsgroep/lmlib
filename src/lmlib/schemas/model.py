from typing import List, Dict
from pydantic import Field
from enum import Enum
from src.lmlib.schemas.base_model import (
    SpatialDefinition, 
    WorkflowSpecification, 
    Area, 
    Equipment, 
    PhysicalAsset, 
    OperationalLocation, 
    StorageZone, 
    WorkflowSpecificationNode, 
    WorkSchedule
)
# Enum for Vessel Type
class VesselType(Enum):
    WINCHESTER = "winchester"
    ATLAS = "atlas"
    EDINBURG = "edinburg"
    SYMPHONY = "symphony"
    LEGACY = "legacy"
    SCOUT = "scout"
    T_CLASS = "T-Class"

class VesselDeckPositionType(Enum):
    """A position on the deck of a vessel."""
    IN_PORT_SIDE = "InPortSide"
    OUTER_PORT_SIDE = "OuterPortSide"
    IN_STARBOARD = "InStarboard"
    OUT_STARBOARD = "OutStarboard"

class VesselResponsibility(Enum):
    MONOPILE_TRANSPORT = "MonopileTransport"
    CRANE_TRANSPORT = "CraneTransport"
    HOOKUP = "Hookup"
    TOWING = "Towing"
    TENSIONING = "Tensioning"
    MOORING = "Mooring"

class WorkTypeEnum(Enum):    
    PRODUCTION = "production"
    MAINTENANCE = "maintenance"
    QUALITY = "quality"
    INVENTORY = "inventory"
    MIXED = "mixed"
    TRANSPORT = "transport"

class WorkScheduleStateEnum(Enum):
    FORECAST = "forecast"
    RELEASED = "released"
    CANCELLED = "cancelled"
    WAITING = "waiting"
    READY = "ready"
    RUNNING = "running"
    COMPLETED = "completed"
    ABORTED = "aborted"
    HELD = "held"
    SUSPENDED = "suspended"
    CLOSED = "closed"

class MonopileStateTransition(WorkflowSpecification):
    """A state transition of a monopile transport for offshore wind farm installation."""
    model_id: str = Field("dtmi:digitaltwins:isa95:MonopileStateTransition;1", const=True)

class FabricationYard(SpatialDefinition, StorageZone):
    """A representation of fabrication yard where the monopiles are stored."""
    model_id: str = Field("dtmi:digitaltwins:isa95:FabricationYard;1", const=True)
    spatial_definition: SpatialDefinition
    monopiles: List["Monopile"]

class Deck(PhysicalAsset):
    """A representation of deck of a vessel."""
    model_id: str = Field("dtmi:digitaltwins:isa95:Deck;1", const=True)
    spatial_definition: SpatialDefinition


class MonopileTransport(WorkflowSpecification):
    """A representation of a monopile transport for offshore wind farm installation."""
    model_id: str = Field("dtmi:digitaltwins:isa95:MonopileTransport;1", const=True)

class DeckPosition(OperationalLocation):
    """A position on the deck of a vessel."""
    model_id: str = Field("dtmi:digitaltwins:isa95:DeckPosition;1", const=True)
    position_type: VesselDeckPositionType
    spatial_definition: SpatialDefinition


class Port(Area, SpatialDefinition):
    """A representation of a port where vessels are docked."""
    model_id: str = Field("dtmi:digitaltwins:isa95:Port;1", const=True)
    spatial_definition: SpatialDefinition

class OffshoreWindFarm(Area, SpatialDefinition):
    """A representation for offshore wind farm installation."""
    model_id: str = Field("dtmi:digitaltwins:isa95:OffshoreWindFarm;1", const=True)
    spatial_definition: SpatialDefinition
    monopiles: List["Monopile"]

class Monopile(Equipment):
    """A representation of a monopile for offshore wind farm installation"""
    model_id: str = Field("dtmi:digitaltwins:isa95:Monopile;1", const=True)
    ID : str
    name: str
    document_number: str
    revision: int
    phase: str
    top_mp_flange: float
    bottom_mp_flange: float
    id: str
    sub_name: str
    dwg_date: str
    site_layout: str
    pe_stamp: str
    mp_length: float
    glauconite: str
    punch_through: str
    design_weight_given: float
    centre_of_gravity_bottom_of_mp: float
    seabed_level_relative_to_water_depth: float
    spatial_definition: SpatialDefinition
    equipment_level: str = "unit"

class MonopileTransportSchedule(WorkSchedule):
    """A representation of monopile transport schedule for offshore wind farm installation."""
    model_id: str = Field("dtmi:digitaltwins:isa95:MonopileTransportSchedule;1", const=True)
    monopile: Monopile
    work_type: WorkTypeEnum
    start_time: str
    end_time: str
    schedule_state: WorkScheduleStateEnum


class Vessel(Equipment):
    """A representation for vessel."""
    model_id: str = Field("dtmi:digitaltwins:isa95:Vessel;1", const=True)
    ID : str
    vessel_type: VesselType
    day_rate: float
    responsibility: VesselResponsibility
    spatial_definition: SpatialDefinition
    port: Port = None
    fabrication_yard: FabricationYard = None
    wind_farm: OffshoreWindFarm = None


class MonopileState(WorkflowSpecificationNode):
    """A state of a monopile transport for offshore wind farm installation."""
    model_id: str = Field("dtmi:digitaltwins:isa95:MonopileState;1", const=True)
    vessel: Vessel
    fabrication_yard: FabricationYard
    monopile_transport_schedule: MonopileTransportSchedule