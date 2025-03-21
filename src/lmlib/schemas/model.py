from typing import List, Dict
from enum import Enum


# class SpatialDefinition:
#     def __init__(self, 
#                  value: str, 
#                  format: str, 
#                  SRID: str = None, 
#                  SRIDauthority: str = None, 
#                  description: Dict = None):
#         self.value = value
#         self.format = format
#         self.SRID = SRID
#         self.SRIDauthority = SRIDauthority
#         self.description = description



class DigitalTwin:
    pass

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


class MonopileStateTransition(DigitalTwin):
    """A state transition of a monopile transport for offshore wind farm installation.""""
    pass


class FabricationYard(DigitalTwin):
    """A representation of fabrication yard where the monopiles are stored."""

    def __init__(self, spatial_definition: SpatialDefinition, monopiles: List['Monopile']):
        self.spatial_definition = spatial_definition
        self.monopiles = monopiles  # relationship with monopiles


class Deck(DigitalTwin):
    """A representation of deck of a vessel."""
    pass


class MonopileTransport(DigitalTwin):
    """A representation of a monopile transport for offshore wind farm installation."""
    pass

class DeckPosition(DigitalTwin):
    """A position on the deck of a vessel."""

    def __init__(self, position_type: VesselDeckPositionType):
        self.position_type = position_type


class Port(DigitalTwin):
    """A representation of a port where vessels are docked."""
    def __init__(self, spatial_definition: SpatialDefinition):
        self.spatial_definition = spatial_definition


class OffshoreWindFarm(DigitalTwin):
    """A representation for offshore wind farm installation."""
    def __init__(self, spatial_definition: SpatialDefinition, monopiles: List['Monopile']):
        self.spatial_definition = spatial_definition
        self.monopiles = monopiles  # relationship with monopiles


class Monopile(DigitalTwin):
    """A representation of a monopile for offshore wind farm installation"""

    def __init__(self, 
                 name: str, 
                 document_number: str, 
                 revision: int, 
                 phase: str, 
                 top_mp_flange: float, 
                 bottom_mp_flange: float,
                 id: str,
                 sub_name: str,
                 dwg_date: str,
                 site_layout: str,
                 pe_stamp: str,
                 mp_length: float,
                 glauconite: str,
                 punch_through: str,
                 design_weight_given: float,
                 centre_of_gravity_bottom_of_mp: float,
                 seabed_level_relative_to_water_depth: float,
                 spatial_definition: SpatialDefinition,
                 equipment_level: str = 'unit',
                ):
        
        self.id = id
        self.name = name
        self.sub_name = sub_name
        self.document_number = document_number
        self.revision = revision
        self.phase = phase

        # Dimensions
        self.top_mp_flange = top_mp_flange
        self.bottom_mp_flange = bottom_mp_flange
        self.mp_length = mp_length

        self.equipment_level = equipment_level
        self.dwg_date = dwg_date
        self.site_layout = site_layout
        self.pe_stamp = pe_stamp

        self.glauconite = glauconite
        self.punch_through = punch_through
        self.design_weight_given = design_weight_given
        self.centre_of_gravity_bottom_of_mp = centre_of_gravity_bottom_of_mp
        self.seabed_level_relative_to_water_depth = seabed_level_relative_to_water_depth
        self.spatial_definition = spatial_definition



class MonopileTransportSchedule(DigitalTwin):
    """A representation of monopile transport schedule for offshore wind farm installation."""
    def __init__(self, monopile: Monopile, work_type: str, start_time: str, end_time: str, schedule_state: str):
        self.monopile = monopile
        self.work_type = work_type
        self.start_time = start_time
        self.end_time = end_time
        self.schedule_state = schedule_state


class Vessel(DigitalTwin):
    """A representation for vessel."""
    def __init__(self, vessel_type: VesselType, day_rate: float, responsibility: str, port: Port, fabrication_yard: FabricationYard, wind_farm: OffshoreWindFarm):
        self.vessel_type = vessel_type
        self.day_rate = day_rate
        self.responsibility = responsibility
        self.port = port
        self.fabrication_yard = fabrication_yard
        self.wind_farm = wind_farm


class MonopileState(DigitalTwin):
    """A state of a monopile transport for offshore wind farm installation."""
    def __init__(self, vessel: Vessel, fabrication_yard: FabricationYard, monopile_transport_schedule: MonopileTransportSchedule):
        self.vessel = vessel
        self.fabrication_yard = fabrication_yard
        self.monopile_transport_schedule = monopile_transport_schedule