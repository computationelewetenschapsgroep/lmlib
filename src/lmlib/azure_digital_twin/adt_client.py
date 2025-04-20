from azure.identity import DefaultAzureCredential
from azure.digitaltwins.core import DigitalTwinsClient
from typing import Optional
import json
from lmlib.utils import singleton


@singleton
class AzureDigitalTwinClient:
    """ Class for interacting with the Azure Digital Twins client. """

    def __init__(self, adt_endpoint: str, credential: Optional[DefaultAzureCredential] = None):
        """
        Singleton class for initializing the DtClient with configuration and credentials.

        :param credential: Azure credentials for authentication (DefaultAzureCredential if None).
        """
        self.credential = credential or DefaultAzureCredential()
        self.adt_endpoint = adt_endpoint
        self.client = self._create_client()

    def _create_client(self) -> DigitalTwinsClient:
        """ Creates and returns a DigitalTwinsClient instance. """
        return DigitalTwinsClient(self.adt_endpoint, self.credential)


@singleton
class AzureDigitalTwinMockClient:
    def __init__(self, twin_graph):
        with open(twin_graph) as f:
            self.digital_twin = json.loads(f)
    
    def list_models(self):
        return self.digital_twin["digitalTwinsModels"]
    
    def get_model(self, model_id):
        result =  [item for item in self.digital_twin['digitalTwinsModels'] if item["@id"]== model_id]
        if result:
            return result.pop()
        else:
            return {}
        
    def decommission_model(model_id):
        raise AttributeError("Decommissioning model is not supported on Mock DT") 
    
    def delete_model(self, model_id: str):
        raise AttributeError("Model deletion is not supported on Mock DT")
    
    def upsert_digital_twin(self, twin_id: str, twin_data: dict):
        raise AttributeError("Model creation is not supported on Mock DT")
    
    def get_digital_twin(self, twin_id: str):
        result = [item for item in self.digital_twin['digitalTwinsGraph']['digitalTwins'] if item['$dtId'] == twin_id]
        if result:
            return result.pop()
        else:
            return {}

    def query_twins(self, twin_id: str):
        raise AttributeError("Query with SQL syntax is not supported on Mock DT")

    def delete_digital_twins(self, twin_id: str):
        raise AttributeError("Deletion  is not supported on Mock DT")
    
    def update_component(self, digital_twin_id: str, component_name: str, patch: list):
        raise AttributeError("Update  is not supported on Mock DT")

    def get_component(self, digital_twin_id: str, component_name: str):
        result = [(component_name,item[component_name]) for item in self.digital_twin['digitalTwinsGraph']['digitalTwins'] if item['$dtId'] == digital_twin_id and component_name in item.keys() ]
        if result:
            return dict(result.pop())
        else:
            return {}
    
    def update_component(self, digital_twin_id: str, component_name: str):
        raise AttributeError("Update  is not supported on Mock DT")

    def delete_relationship(self, source_id : str,relationship_id:str):
        raise AttributeError("Delete relationship not possible on MockDT")
    
    def upsert_relationship(self, source_id: str, relationship_id: str, relationship_data: dict):
        raise AttributeError("Upsert relationship not possible on MockDT")

    def list_relationships(self, digital_twin_id):
        result =  [item for item in self.digital_twin['digitalTwinsGraph']['relationships'] if item['$sourceId'] == digital_twin_id]
        return result
    
    def list_incoming_relationships(self, digital_twin_id):
        result = [item for item in self.digital_twin['digitalTwinsGraph']['relationships'] if item['$targetId'] == digital_twin_id]
        return result

    def list_event_routes(self):
        raise AttributeError("List event route  not possible on MockDT")

    def delete_event_routes(self, event_route_id: str):
        raise AttributeError("Delete event route relationship not possible on MockDT")
