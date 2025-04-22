import pytest
from azure.identity import DefaultAzureCredential
from azure.digitaltwins.core import DigitalTwinsClient
from lmlib.azure_digital_twin.adt_service import AzureDigitalTwinsService
from azure.digitaltwins.core._generated.models._models_py3 import DigitalTwinsModelData


@pytest.fixture
def mock_credentials(mocker):
    return mocker.MagicMock(spec=DefaultAzureCredential)


@pytest.fixture
def mock_adt_client(mocker):
    return mocker.patch('lmlib.azure_digital_twin.adt_service.AzureDigitalTwinClient')


@pytest.fixture
def mock_digital_twins_client(mocker):
    return mocker.MagicMock(spec=DigitalTwinsClient)


def test_azure_digital_twins_service_initialization(mock_adt_client, mock_credentials, mocker):
    adt_endpoint = "https://test-adt-endpoint.com"
    
    mock_client_manager = mocker.MagicMock()
    mock_adt_client.return_value = mock_client_manager
    
    service = AzureDigitalTwinsService(adt_endpoint, credential=mock_credentials)
    
    mock_adt_client.assert_called_once_with(adt_endpoint=adt_endpoint, credential=mock_credentials)
    
    assert service.client_manager == mock_client_manager
    assert service.client is mock_client_manager.client


def test_list_models(mock_adt_client, mock_digital_twins_client, mocker):
    """Test the list_models method of AzureDigitalTwinsService."""
    adt_endpoint = "https://test-adt-endpoint.com"
    
    mock_client_manager = mocker.MagicMock()
    mock_adt_client.return_value = mock_client_manager
    
    mock_client = mocker.MagicMock(spec=DigitalTwinsClient)
    mock_client_manager.client = mock_client
    

    mocked_models = [
        mocker.MagicMock(
            spec=DigitalTwinsModelData, 
            as_dict=mocker.MagicMock(
                return_value={"id": "model_1", "display_name": {"en": "Model 1"}}
            )
        ),
        mocker.MagicMock(
            spec=DigitalTwinsModelData, 
            as_dict=mocker.MagicMock(
                return_value={"id": "model_2", "display_name": {"en": "Model 2"}}
            )
        )
    ]
    mock_client.list_models.return_value = mocked_models
    
    service = AzureDigitalTwinsService(adt_endpoint)
    
    all_models = service.list_models()
    
    mock_client.list_models.assert_called_once()
    
    list_of_models = [model for model in all_models]
    
    assert len(list_of_models) == 2
    assert list_of_models[0].as_dict() == {"id": "model_1", "display_name": {"en": "Model 1"}}
    assert list_of_models[1].as_dict() == {"id": "model_2", "display_name": {"en": "Model 2"}}


def test_list_models_empty(mock_adt_client, mock_digital_twins_client, mocker):
    adt_endpoint = "https://test-adt-endpoint.com"
    
    mock_client_manager = mocker.MagicMock()
    mock_adt_client.return_value = mock_client_manager
    
    mock_client = mocker.MagicMock(spec=DigitalTwinsClient)
    mock_client_manager.client = mock_client
    
    mock_client.list_models.return_value = []
    
    service = AzureDigitalTwinsService(adt_endpoint)
    
    all_models = service.list_models()
    
    mock_client.list_models.assert_called_once()
    
    assert not all_models


def test_get_model(mock_adt_client, mock_digital_twins_client, mocker):
    adt_endpoint = "https://test-adt-endpoint.com"
    model_id = "dtmi:digitaltwins:isa95:ext:Tags;1"
    
    mock_client_manager = mocker.MagicMock()
    mock_adt_client.return_value = mock_client_manager
    
    mock_client = mocker.MagicMock(spec=DigitalTwinsClient)
    mock_client_manager.client = mock_client
    
    mock_model = mocker.MagicMock(spec=DigitalTwinsModelData, as_dict=mocker.MagicMock(return_value={"id": model_id, "display_name": {"en": "Tags"}}))
    mock_client.get_model.return_value = mock_model
    
    service = AzureDigitalTwinsService(adt_endpoint)
    
    model = service.get_model(model_id)
    
    mock_client.get_model.assert_called_once_with(model_id)
    
    assert model.as_dict() == {"id": model_id, "display_name": {"en": "Tags"}}


def test_get_model_error(mock_adt_client, mock_digital_twins_client, mocker):
    adt_endpoint = "https://test-adt-endpoint.com"
    model_id = "dtmi:digitaltwins:isa95:ext:Tags;1"
    
    
    mock_client_manager = mocker.MagicMock()
    mock_adt_client.return_value = mock_client_manager
    
    
    mock_client = mocker.MagicMock(spec=DigitalTwinsClient)
    mock_client_manager.client = mock_client
    mock_client.get_model.side_effect = Exception(f"Error retrieving model {model_id}")
    
    
    service = AzureDigitalTwinsService(adt_endpoint)
    
    
    with pytest.raises(Exception, match=f"Error retrieving model {model_id}"):
        service.get_model(model_id)


def test_decommission_model(mock_adt_client, mock_digital_twins_client, mocker):
    """Test the decommission_model method of AzureDigitalTwinsService."""
    adt_endpoint = "https://test-adt-endpoint.com"
    model_id = "dtmi:digitaltwins:isa95:ext:Tags;1"
    
    
    mock_client_manager = mocker.MagicMock()
    mock_adt_client.return_value = mock_client_manager
    
    
    mock_client = mocker.MagicMock(spec=DigitalTwinsClient)
    mock_client_manager.client = mock_client
    
    
    mock_client.decommission_model.return_value = None
    
    
    service = AzureDigitalTwinsService(adt_endpoint)
    
    
    service.decommission_model(model_id)
    
    
    mock_client.decommission_model.assert_called_once_with(model_id)


def test_decommission_model_error(mock_adt_client, mock_digital_twins_client, mocker):
    """Test the decommission_model method of AzureDigitalTwinsService when an error occurs."""
    adt_endpoint = "https://test-adt-endpoint.com"
    model_id = "dtmi:digitaltwins:isa95:ext:Tags;1"
    
    
    mock_client_manager = mocker.MagicMock()
    mock_adt_client.return_value = mock_client_manager
    
    
    mock_client = mocker.MagicMock(spec=DigitalTwinsClient)
    mock_client_manager.client = mock_client
    mock_client.decommission_model.side_effect = Exception(f"Error decommissioning model {model_id}")
    
    
    service = AzureDigitalTwinsService(adt_endpoint)
    
    
    with pytest.raises(Exception, match=f"Error decommissioning model {model_id}"):
        service.decommission_model(model_id)


def test_delete_model(mock_adt_client, mock_digital_twins_client, mocker):
    """Test the delete_model method of AzureDigitalTwinsService."""
    adt_endpoint = "https://test-adt-endpoint.com"
    model_id = "dtmi:digitaltwins:isa95:ext:Tags;1"
    
    
    mock_client_manager = mocker.MagicMock()
    mock_adt_client.return_value = mock_client_manager
    
    
    mock_client = mocker.MagicMock(spec=DigitalTwinsClient)
    mock_client_manager.client = mock_client
    
    
    mock_client.delete_model.return_value = None
    
    
    service = AzureDigitalTwinsService(adt_endpoint)
    
    
    service.delete_model(model_id)
    
    
    mock_client.delete_model.assert_called_once_with(model_id)


def test_delete_model_error(mock_adt_client, mock_digital_twins_client, mocker):
    """Test the delete_model method of AzureDigitalTwinsService when an error occurs."""
    adt_endpoint = "https://test-adt-endpoint.com"
    model_id = "dtmi:digitaltwins:isa95:ext:Tags;1"
    
    
    mock_client_manager = mocker.MagicMock()
    mock_adt_client.return_value = mock_client_manager
    
    
    mock_client = mocker.MagicMock(spec=DigitalTwinsClient)
    mock_client_manager.client = mock_client
    mock_client.delete_model.side_effect = Exception(f"Error deleting model {model_id}")
    
    
    service = AzureDigitalTwinsService(adt_endpoint)
    
    
    with pytest.raises(Exception, match=f"Error deleting model {model_id}"):
        service.delete_model(model_id)


def test_get_digital_twin(mock_adt_client, mock_digital_twins_client, mocker):
    """Test the get_digital_twin method of AzureDigitalTwinsService."""
    adt_endpoint = "https://test-adt-endpoint.com"
    twin_id = "twin_1"
    
    
    mock_client_manager = mocker.MagicMock()
    mock_adt_client.return_value = mock_client_manager
    
    
    mock_client = mocker.MagicMock(spec=DigitalTwinsClient)
    mock_client_manager.client = mock_client
    
    
    mock_twin = mocker.MagicMock()
    mock_client.get_digital_twin.return_value = mock_twin
    
    
    service = AzureDigitalTwinsService(adt_endpoint)
    
    
    twin = service.get_digital_twin(twin_id)
    
    
    mock_client.get_digital_twin.assert_called_once_with(twin_id)
    
    
    assert twin == mock_twin


def test_get_digital_twin_error(mock_adt_client, mock_digital_twins_client, mocker):
    """Test the get_digital_twin method of AzureDigitalTwinsService when an error occurs."""
    adt_endpoint = "https://test-adt-endpoint.com"
    twin_id = "twin_1"
    
    
    mock_client_manager = mocker.MagicMock()
    mock_adt_client.return_value = mock_client_manager
    
    
    mock_client = mocker.MagicMock(spec=DigitalTwinsClient)
    mock_client_manager.client = mock_client
    mock_client.get_digital_twin.side_effect = Exception(f"Error retrieving digital twin {twin_id}")
    
    
    service = AzureDigitalTwinsService(adt_endpoint)
    
    
    with pytest.raises(Exception, match=f"Error retrieving digital twin {twin_id}"):
        service.get_digital_twin(twin_id)


def test_query_digital_twins(mock_adt_client, mock_digital_twins_client, mocker):
    """Test the query_digital_twins method of AzureDigitalTwinsService."""
    adt_endpoint = "https://test-adt-endpoint.com"
    query_expression = "SELECT * FROM digitaltwins WHERE condition = true"
    
    
    mock_client_manager = mocker.MagicMock()
    mock_adt_client.return_value = mock_client_manager
    
    
    mock_client = mocker.MagicMock(spec=DigitalTwinsClient)
    mock_client_manager.client = mock_client
    
    
    mock_query_result = ["result_1", "result_2"]
    mock_client.query_twins.return_value = mock_query_result
    
    
    service = AzureDigitalTwinsService(adt_endpoint)
    
    
    query_result = service.query_digital_twins(query_expression)
    
    
    mock_client.query_twins.assert_called_once_with(query_expression)
    
    
    assert query_result == mock_query_result

def test_update_digital_twin_component(mock_adt_client, mock_digital_twins_client, mocker):
    """Test the update_digital_twin_component method of AzureDigitalTwinsService."""
    adt_endpoint = "https://test-adt-endpoint.com"
    twin_id = "twin_1"
    component_name = "component_1"
    patch = [{"op": "replace", "path": "/property1", "value": "new_value"}]
    
    
    mock_client_manager = mocker.MagicMock()
    mock_adt_client.return_value = mock_client_manager
    
    
    mock_client = mocker.MagicMock(spec=DigitalTwinsClient)
    mock_client_manager.client = mock_client
    
    
    mock_client.update_component.return_value = None
    
    
    service = AzureDigitalTwinsService(adt_endpoint)
    
    
    service.update_digital_twin_component(twin_id, component_name, patch)
    
    
    mock_client.update_component.assert_called_once_with(twin_id, component_name, patch)


def test_get_digital_twin_component(mock_adt_client, mock_digital_twins_client, mocker):
    """Test the get_digital_twin_component method of AzureDigitalTwinsService."""
    adt_endpoint = "https://test-adt-endpoint.com"
    twin_id = "twin_1"
    component_name = "component_1"
    
    
    mock_client_manager = mocker.MagicMock()
    mock_adt_client.return_value = mock_client_manager
    
    
    mock_client = mocker.MagicMock(spec=DigitalTwinsClient)
    mock_client_manager.client = mock_client
    
    
    mock_component = mocker.MagicMock()
    mock_client.get_component.return_value = mock_component
    
    
    service = AzureDigitalTwinsService(adt_endpoint)
    
    
    component = service.get_digital_twin_component(twin_id, component_name)
    
    
    mock_client.get_component.assert_called_once_with(twin_id, component_name)
    
    
    assert component == mock_component

def test_create_relationship(mock_adt_client, mock_digital_twins_client, mocker):
    """Test the create_relationship method of AzureDigitalTwinsService."""
    adt_endpoint = "https://test-adt-endpoint.com"
    source_id = "source_twin_1"
    relationship_id = "relationship_1"
    relationship_data = {"property": "value"}
    
    
    mock_client_manager = mocker.MagicMock()
    mock_adt_client.return_value = mock_client_manager
    
    
    mock_client = mocker.MagicMock(spec=DigitalTwinsClient)
    mock_client_manager.client = mock_client
    
    
    mock_client.upsert_relationship.return_value = None
    
    
    service = AzureDigitalTwinsService(adt_endpoint)
    
    
    service.create_relationship(source_id, relationship_id, relationship_data)
    
    
    mock_client.upsert_relationship.assert_called_once_with(source_id, relationship_id, relationship_data)

def test_delete_relationship(mock_adt_client, mock_digital_twins_client, mocker):
    """Test the delete_relationship method of AzureDigitalTwinsService."""
    adt_endpoint = "https://test-adt-endpoint.com"
    twin_id = "twin_1"
    relationship_id = "relationship_1"
    
    
    mock_client_manager = mocker.MagicMock()
    mock_adt_client.return_value = mock_client_manager
    
    
    mock_client = mocker.MagicMock(spec=DigitalTwinsClient)
    mock_client_manager.client = mock_client
    
    
    mock_client.delete_relationship.return_value = None
    
    
    service = AzureDigitalTwinsService(adt_endpoint)
    
    
    service.delete_relationship(twin_id, relationship_id)
    
    
    mock_client.delete_relationship.assert_called_once_with(twin_id, relationship_id)

def test_list_relationships(mock_adt_client, mock_digital_twins_client, mocker):
    """Test the list_relationships method of AzureDigitalTwinsService."""
    adt_endpoint = "https://test-adt-endpoint.com"
    twin_id = "twin_1"
    
    
    mock_client_manager = mocker.MagicMock()
    mock_adt_client.return_value = mock_client_manager
    
    
    mock_client = mocker.MagicMock(spec=DigitalTwinsClient)
    mock_client_manager.client = mock_client
    
    
    mock_relationships = ["relationship_1", "relationship_2"]
    mock_client.list_relationships.return_value = mock_relationships
    
    
    service = AzureDigitalTwinsService(adt_endpoint)
    
    
    relationships = service.list_relationships(twin_id)
    
    
    mock_client.list_relationships.assert_called_once_with(twin_id)
    
    
    assert relationships == mock_relationships


def test_list_incoming_relationships(mock_adt_client, mock_digital_twins_client, mocker):
    """Test the list_incoming_relationships method of AzureDigitalTwinsService."""
    adt_endpoint = "https://test-adt-endpoint.com"
    twin_id = "twin_1"
    
    
    mock_client_manager = mocker.MagicMock()
    mock_adt_client.return_value = mock_client_manager
    
    
    mock_client = mocker.MagicMock(spec=DigitalTwinsClient)
    mock_client_manager.client = mock_client
    
    
    mock_incoming_relationships = ["incoming_relationship_1", "incoming_relationship_2"]
    mock_client.list_incoming_relationships.return_value = mock_incoming_relationships
    
    
    service = AzureDigitalTwinsService(adt_endpoint)
    
    
    incoming_relationships = service.list_incoming_relationships(twin_id)
    
    
    mock_client.list_incoming_relationships.assert_called_once_with(twin_id)
    
    
    assert incoming_relationships == mock_incoming_relationships

def test_create_event_route(mock_adt_client, mock_digital_twins_client, mocker):
    """Test the create_event_route method of AzureDigitalTwinsService."""
    adt_endpoint = "https://test-adt-endpoint.com"
    event_route_id = "event_route_1"
    route_data = {"property": "value"}
    
    
    mock_client_manager = mocker.MagicMock()
    mock_adt_client.return_value = mock_client_manager
    
    
    mock_client = mocker.MagicMock(spec=DigitalTwinsClient)
    mock_client_manager.client = mock_client
    
    
    mock_client.upsert_event_route.return_value = None
    
    
    service = AzureDigitalTwinsService(adt_endpoint)
    
    
    service.create_event_route(event_route_id, route_data)
    
    
    mock_client.upsert_event_route.assert_called_once_with(event_route_id, route_data)


def test_list_event_routes(mock_adt_client, mock_digital_twins_client, mocker):
    """Test the list_event_routes method of AzureDigitalTwinsService."""
    adt_endpoint = "https://test-adt-endpoint.com"
    
    
    mock_client_manager = mocker.MagicMock()
    mock_adt_client.return_value = mock_client_manager
    
    
    mock_client = mocker.MagicMock(spec=DigitalTwinsClient)
    mock_client_manager.client = mock_client
    
    
    mock_event_routes = ["event_route_1", "event_route_2"]
    mock_client.list_event_routes.return_value = mock_event_routes
    
    
    service = AzureDigitalTwinsService(adt_endpoint)
    
    
    event_routes = service.list_event_routes()
    
    
    mock_client.list_event_routes.assert_called_once()
    
    
    assert event_routes == mock_event_routes


def test_delete_event_route(mock_adt_client, mock_digital_twins_client, mocker):
    """Test the delete_event_route method of AzureDigitalTwinsService."""
    adt_endpoint = "https://test-adt-endpoint.com"
    event_route_id = "event_route_1"
    
    
    mock_client_manager = mocker.MagicMock()
    mock_adt_client.return_value = mock_client_manager
    
    
    mock_client = mocker.MagicMock(spec=DigitalTwinsClient)
    mock_client_manager.client = mock_client
    
    
    mock_client.delete_event_route.return_value = None
    
    
    service = AzureDigitalTwinsService(adt_endpoint)
    
    
    service.delete_event_route(event_route_id)
    
    
    mock_client.delete_event_route.assert_called_once_with(event_route_id)
