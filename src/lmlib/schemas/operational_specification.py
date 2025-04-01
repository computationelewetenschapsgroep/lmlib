from pydantic import BaseModel, field_validator, Field
from datetime import datetime
from enum import Enum

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
    model_id: str =  Field("dtmi:digitaltwins:isa95:OperationsDefinition;1", Literal=True)

class OperationsSegment(OperationsDefinition):
    duration : str
    duration_unit_of_measure: str
    model_id: str =  Field("dtmi:digitaltwins:isa95:OperationsSegment;1", Literal=True)


class ParameterSpecification(BaseModel):
    value: str
    value_unit_of_measure: str
    model_id: str =  Field("dtmi:digitaltwins:isa95:ParameterSpecification;1", Literal=True)


class GrillageCompatibility(ParameterSpecification):
    grillage_type: GrillageType
    model_id: str =  Field("dtmi:digitaltwins:isa95:GrillageCompatibility;1", Literal=True)




