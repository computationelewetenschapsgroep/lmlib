from unittest.mock import MagicMock
from src.lmlib.schemas.model import ParameterSpecification, GrillageCompatibility
from src.lmlib.schemas.model import Decklength, Monopile, FabricationYard, GrillageType
from src.lmlib.eta_calculator.deterministic.monopile.configurations import GrillageConfigurations, LengthConfigurations, Operand, camel_case_to_snake_case

def mock_query_digital_twins(query: str):
    if "select * from digitaltwins" in query:
        return [
            {"$dtId": "twin_1", "value": "20", "valueUnitOfMeasure": "percentage", "grillageType": "SRW"},
            {"$dtId": "twin_2", "value": "30", "valueUnitOfMeasure": "percentage", "grillageType": "type_B"}
        ]
    elif "SELECT target FROM digitaltwins source JOIN target RELATED" in query:
        return [
                {
                    "target": 
                        # {
                        #     '$dt_id': 'twin123',
                        #     'spatial_definition': {
                        #         'value': "POINT(80 40)"
                        #     },
                        #     'status': 'Installed',
                        #     'document_number': 'DOC-001',
                        #     'revision': 1,
                        #     'name': 'Monopile A',
                        #     'sub_name': 'Subpart A1',
                        #     'dwg_date': '2023-03-25',
                        #     'site_layout': 'Site layout 1',
                        #     'phase': 'Phase 1',
                        #     'pe_stamp': 'PE-XYZ',
                        #     'top_mp_flange': 10.5,
                        #     'bottom_mp_flange': 12.0,
                        #     'mp_length': 100,
                        #     'glauconite': "True",
                        #     'punch_through': "False",
                        #     'design_weight_given': 50000,
                        #     'centre_of_gravity_bottom_of_mp': 35.5,
                        #     'seabed_level_relative_to_water_depth': 25.0,
                        # }
                        {"$dtId": "twin_1", "value": "20", "valueUnitOfMeasure": "percentage", "grillageType": "SRW"},

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

import pytest
from azure.digitaltwins.core import DigitalTwinsClient
from lmlib.azure_digital_twin.adt_service import AzureDigitalTwinsService
from azure.digitaltwins.core._generated.models._models_py3 import DigitalTwinsModelData

@pytest.fixture
def mock_adt_client(mocker):
    return mocker.patch('lmlib.azure_digital_twin.adt_service.AzureDigitalTwinClient')

# def mock_query_adt_service(mocker):
#     adt_endpoint = "https://test-adt-endpoint.com"
#     query_expression = "SELECT * FROM digitaltwins WHERE condition = true"
#     mock_client_manager = mocker.MagicMock()
#     mock_adt_client.return_value = mock_client_manager
#     mock_client = mocker.MagicMock(spec=DigitalTwinsClient)
#     mock_client_manager.client = mock_client
#     mock_client.query_twins.return_value = mock_query_digital_twins
#     service = AzureDigitalTwinsService(adt_endpoint)
#     query_result = service.query_digital_twins(query_expression)
#     return service

def mock_query_adt_service():
    service = MagicMock()
    service.query_digital_twins = mock_query_digital_twins
    return service


def test_operand_class(mocker):
    # Source should be of the type class ParameterSpecification, like GrillageCompatibility
    # target can be Monopile/FabricationYard
    adt_service = mock_query_adt_service()
    operand = Operand(adt_service, GrillageCompatibility, "grillage_type", "twin_1", "of")
    assert len(operand.get()) > 0
    assert isinstance(operand.get()[0], GrillageCompatibility)

def test_operand_with_invalid_property(mocker):
    adt_service = mock_query_adt_service()

    with pytest.raises(ValueError, match="Property 'grillage_area' is not defined in target type 'GrillageCompatibility'"):
        Operand(adt_service, GrillageCompatibility, "grillage_area", "twin_1", "of")

def test_operand_with_invalid_class_target(mocker):
    adt_service = mock_query_adt_service()
    with pytest.raises(TypeError, match="Target type must be a subclass of ParameterSpecification"):
        Operand(adt_service, Monopile, "grillage_type", "twin_1", "of")


