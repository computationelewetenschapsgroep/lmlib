from pydantic import BaseModel, Field
from enum import Enum
from typing import ClassVar, Literal

class OperationsDefinitionType(Enum):
    PATTERN = "pattern"
    INSTANCE = "instance"

class OperationsType(Enum):
    PRODUCTION= "production"


class GrillageType(Enum):
    REV = "REV"
    SRW = "SRW"    


class OperationsDefinition(BaseModel):
    definition_type: OperationsDefinitionType
    operations_type: OperationsType
    model_id: ClassVar[Literal['dtmi:digitaltwins:isa95:OperationsDefinition;1']] = 'dtmi:digitaltwins:isa95:OperationsDefinition;1'


class OperationsSegment(OperationsDefinition):
    duration : str
    duration_unit_of_measure: str
    model_id: ClassVar[Literal['dtmi:digitaltwins:isa95:OperationsSegment;1']] = 'dtmi:digitaltwins:isa95:OperationsSegment;1'


class ParameterSpecification(BaseModel):
    model_id: ClassVar[Literal['dtmi:digitaltwins:isa95:ParameterSpecification;1']] = 'dtmi:digitaltwins:isa95:ParameterSpecification;1'
    value: str
    value_unit_of_measure: str
    is_active: bool = False

class GrillageCompatibility(ParameterSpecification):
    model_id: ClassVar[Literal['dtmi:digitaltwins:isa95:GrillageCompatibility;1']] = 'dtmi:digitaltwins:isa95:GrillageCompatibility;1'
    grillage_type: GrillageType
    is_active: bool = False




