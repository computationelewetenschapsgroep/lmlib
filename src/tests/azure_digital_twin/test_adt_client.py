import pytest
from lmlib.azure_digital_twin.adt_client import AzureDigitalTwinClient
from azure.identity import DefaultAzureCredential

@pytest.fixture
def mock_credentials(mocker):
    return mocker.MagicMock(spec=DefaultAzureCredential)

@pytest.fixture
def mock_digital_twins_client(mocker):
    return mocker.patch('lmlib.azure_digital_twin.adt_client.DigitalTwinsClient')

@pytest.fixture
def mock_default_credential(mocker):
    return mocker.patch('lmlib.azure_digital_twin.adt_client.DefaultAzureCredential')

def test_default_credential_initialization(mock_default_credential, mock_digital_twins_client):
    endpoint = "https://default-cred-endpoint.com"
    
    client = AzureDigitalTwinClient(endpoint)
    
    mock_default_credential.assert_called_once()
    mock_digital_twins_client.assert_called_once_with(endpoint, mock_default_credential.return_value)
    assert client.credential is mock_default_credential.return_value


def test_client_reuse(mock_digital_twins_client):
    """Verify the same client is reused across instances"""
    instance1 = AzureDigitalTwinClient("https://endpoint.com")
    instance2 = AzureDigitalTwinClient("https://endpoint.com")
    
    assert instance1.client is instance2.client


def test_singleton_behavior(mock_credentials, mocker):
    """Test that only one instance is created regardless of call arguments"""
    instance1 = AzureDigitalTwinClient("https://default-cred-endpoint.com", mock_credentials)
    instance2 = AzureDigitalTwinClient("https://default-cred-endpoint-2.com", mocker.MagicMock())
    instance3 = AzureDigitalTwinClient("https://default-cred-endpoint-3.com")
    
    assert instance1 is instance2 is instance3
    assert instance1.adt_endpoint == "https://default-cred-endpoint.com"
