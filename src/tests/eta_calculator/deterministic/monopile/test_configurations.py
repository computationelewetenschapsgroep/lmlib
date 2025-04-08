import pytest
from unittest.mock import MagicMock
from src.lmlib.schemas.model import GrillageTypeEnum, ParameterSpecification, GrillageCompatibility
from src.lmlib.schemas.model import Decklength, Monopile, FabricationYard, GrillageType
from src.lmlib.eta_calculator.deterministic.monopile.configurations import GrillageConfigurations, LengthConfigurations, Operand, camel_case_to_snake_case

def mock_query_digital_twins(query: str):
    if "select * from digitaltwins" in query:
        return [
            {"$dtId": "twin_1", "value": "20", "valueUnitOfMeasure": "percentage", "grillageType": "SRW"},
            {"$dtId": "twin_2", "value": "30", "valueUnitOfMeasure": "percentage", "grillageType": "type_B"}
        ]
    elif "SELECT target FROM digitaltwins source JOIN target RELATED source.ofFabricationYard" in query:
        return [
            {
                "target" :
                    {
                        '$dtId': 'twin_fab_1',
                        'value': 'POINT(80 40)',
                        'format': 'WKT' ,
                        'spatialDefinition': {
                            'value': 'POINT(80 40)',
                            'format': 'WKT' 
                        }
                    }
            }
        ]
    elif "SELECT target FROM digitaltwins source JOIN target RELATED source.with where source.$dtId='twin_fab_1'" in query:
        return [
            {
                "target" :
                    # {
                    #     '$dtId': 'twin1',
                    #     'value': 'POINT(80 40)',
                    #     'format': 'WKT' ,
                    #     'spatialDefinition': {
                    #         'value': 'POINT(80 40)',
                    #         'format': 'WKT' 
                    #     }
                    # }
                    {"$dtId": "twin_1", "value": "20", "valueUnitOfMeasure": "percentage", "grillageType": "SRW"}
            }
        ]
    elif "SELECT target FROM digitaltwins source JOIN target RELATED source.of" in query:
        return [
                {
                    "target": 
                        {
                            '$dtId': 'twin123',
                            'value': "POINT(80 40)",
                            'format': 'WKT' ,
                            'spatialDefinition': {
                                'value': "POINT(80 40)",
                                'format': 'WKT' 
                            },
                            'status': 'Installed',
                            'documentNumber': 'DOC-001',
                            'revision': 1,
                            'name': 'Monopile A',
                            'subName': 'Subpart A1',
                            'dwgDate': '2023-03-25',
                            'siteLayout': 'Site layout 1',
                            'phase': 'Phase 1',
                            'peStamp': 'PE-XYZ',
                            'topMpFlange': 10.5,
                            'bottomMpFlange': 12.0,
                            'mpLength': 30,
                            'glauconite': "True",
                            'punchThrough': "False",
                            'designWeightGiven': 50000,
                            'centreOfGravityBottomOfMp': 35.5,
                            'seabedLevelRelativeToWaterDepth': 25.0,
                        }
                        # {"$dtId": "twin_1", "value": "20", "valueUnitOfMeasure": "percentage", "grillageType": "SRW"},

                }

            ]
    elif "SELECT target FROM digitaltwins source JOIN target RELATED source.with" in query:
        return [
                {
                    "target": 
                        {
                            '$dtId': 'twin123',
                            'value': '40',
                            'valueUnitOfMeasure': 'percentage'
                        }

                }

            ]
        # return [
        #         {
        #             "target": {
        #                 '$dtId': 'twin123',
        #                 'spatialDefinition': {
        #                     'value': "POINT(80 40)"
        #                 },
        #                 'status': 'Installed',
        #                 'documentNumber': 'DOC-001',
        #                 'revision': 1,
        #                 'name': 'Monopile A',
        #                 'subName': 'Subpart A1',
        #                 'dwgDate': '2023-03-25',
        #                 'siteLayout': 'Site layout 1',
        #                 'phase': 'Phase 1',
        #                 'peStamp': 'PE-XYZ',
        #                 'topMPFlange': 10.5,
        #                 'bottomMPFlange': 12.0,
        #                 'mpLength': 100,
        #                 'glauconite': "True",
        #                 'punchThrough': "False",
        #                 'designWeightGiven': 50000,
        #                 'centreOfGravityBottomofMP': 35.5,
        #                 'seabedLevelRelativetoWaterDepth': 25.0,
        #             }   
        #         }
        #     ]
        # return [
        #     {"$dtId": "twin_1", "value": "20", "valueUnitOfMeasure": "percentage", "grillageType": "type_A"},
        #     {"$dtId": "twin_2", "value": "30", "valueUnitOfMeasure": "percentage", "grillageType": "type_B"}
        # ]
    return []

def mock_adt_service():
    service = MagicMock()
    service.query_digital_twins = mock_query_digital_twins
    return service


@pytest.fixture
def mock_adt_client(mocker):
    return mocker.patch('lmlib.azure_digital_twin.adt_service.AzureDigitalTwinClient')

def mock_query_adt_service():
    service = MagicMock()
    service.query_digital_twins = mock_query_digital_twins
    return service


def test_operand_class(mocker):
    # Source should be of the type class ParameterSpecification, like GrillageCompatibility
    # target can be Monopile/FabricationYard
    adt_service = mock_query_adt_service()
    operand = Operand(adt_service, Monopile, "mp_length", "twin_1", "of")
    assert len(operand.get()) > 0
    assert isinstance(operand.get()[0], Monopile)

def test_operand_with_invalid_property(mocker):
    adt_service = mock_query_adt_service()

    with pytest.raises(ValueError, match="Property 'grillage_area' is not defined in target type 'GrillageCompatibility'"):
        Operand(adt_service, GrillageCompatibility, "grillage_area", "twin_1", "of")

def test_length_configurations():
    adt_service = mock_adt_service()
    length_config = LengthConfigurations(adt_service, "twin_1", Monopile, "mp_length", Decklength, "value")
    assert len(length_config.get()) > 0
    assert isinstance(length_config.get()[0], tuple)

def test_length_configurations_is_compatible():
    class Dummy:
        def model_dump(self):
            return {
                "mp_length": 1,
                "value" : 5
            }

    elem = (Dummy(), Dummy())
    scale_factor = 1.1
    property_lop = "mp_length"
    property_rop = "value"

    result = LengthConfigurations.is_compatible(elem, scale_factor, property_lop, property_rop)
    assert result is True 


def test_length_configurations_missing_data(mocker):
    mock_adt_service = mocker.MagicMock()
    mock_adt_service.query_digital_twins.return_value = []
    mock_operand = mocker.patch('src.lmlib.eta_calculator.deterministic.monopile.configurations.Operand')
    mock_operand_instance = mock_operand.return_value
    length_config = LengthConfigurations(mock_adt_service, "twin_1", Monopile, "mp_length", Decklength, "value")
    assert length_config.configurations == []
    mock_adt_service.query_digital_twins.assert_called_once()
    mock_operand_instance.get.assert_not_called()


def test_grillage_configurations():
    adt_service = mock_adt_service()
    grillage_config = GrillageConfigurations(adt_service, "twin_fab_1", FabricationYard, "id", GrillageType, "grillage_type")

    assert len(grillage_config.get()) > 0
    assert isinstance(grillage_config.get()[0], tuple)


def test_grillage_configurations_missing_data(mocker):
    mock_adt_service = mocker.MagicMock()
    mock_adt_service.query_digital_twins.return_value = []
    mock_operand = mocker.patch('src.lmlib.eta_calculator.deterministic.monopile.configurations.Operand')
    mock_operand_instance = mock_operand.return_value
    length_config = GrillageConfigurations(mock_adt_service, "twin_1", Monopile, "mp_length", Decklength, "value")
    assert length_config.configurations == []
    mock_adt_service.query_digital_twins.assert_called_once()
    mock_operand_instance.get.assert_not_called()

def test_camel_case_to_snake_case():
    assert camel_case_to_snake_case("topMpFlange") == "top_mp_flange"

def test_parameter_specification():
    param_spec = ParameterSpecification(value="20", value_unit_of_measure="percentage")
    assert param_spec.value == "20"
    assert param_spec.value_unit_of_measure == "percentage"
    assert param_spec.model_id == "dtmi:digitaltwins:isa95:ParameterSpecification;1"

def test_grillage_compatibility():
    grillage_compat = GrillageCompatibility(value="20", value_unit_of_measure="percentage", grillage_type="SRW")
    assert grillage_compat.value == "20"
    assert grillage_compat.value_unit_of_measure == "percentage"
    assert grillage_compat.grillage_type == GrillageTypeEnum.SRW
    assert grillage_compat.model_id == "dtmi:digitaltwins:isa95:GrillageCompatibility;1"
