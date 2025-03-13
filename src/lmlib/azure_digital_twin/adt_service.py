import uuid
from typing import Optional
from azure.identity import DefaultAzureCredential
from azure_digital_twin.adt_client import AzureDigitalTwinClient


class AzureDigitalTwinsService:
    def __init__(self, adt_endpoint: str, credential: Optional[DefaultAzureCredential] = None):
        self.client_manager = AzureDigitalTwinClient(adt_endpoint=adt_endpoint,credential=credential)
        self.client = self.client_manager.client

    def list_models(self):
        """ List all models in the Azure Digital Twins instance. """
        listed_models = self.client.list_models()
        return listed_models

    def get_model(self, model_id: str):
        """ Get a specific model by model_id. """
        try:
            model = self.client.get_model(model_id)
            return model
        except Exception as e:
            print(f"Error retrieving model {model_id}: {e}")
            raise

    def decommission_model(self, model_id: str):
        """ Decommission a model by its model_id. """
        try:
            self.client.decommission_model(model_id)
            print(f"Model {model_id} decommissioned successfully.")
        except Exception as e:
            print(f"Error decommissioning model {model_id}: {e}")
            raise

    def delete_model(self, model_id: str):
        """ Delete a model by its model_id. """
        try:
            self.client.delete_model(model_id)
            print(f"Model {model_id} deleted successfully.")
        except Exception as e:
            print(f"Error deleting model {model_id}: {e}")
            raise

    def create_digital_twin(self, model_id: str, twin_data: dict):
        """ Create a digital twin based on a model. """
        digital_twin_id = 'digitalTwin-' + str(uuid.uuid4())
        twin_data["$metadata"] = {"$model": model_id}
        twin_data["$dtId"] = digital_twin_id
        
        try:
            created_twin = self.client.upsert_digital_twin(digital_twin_id, twin_data)
            return created_twin
        except Exception as e:
            print(f"Error creating digital twin: {e}")
            raise

    def get_digital_twin(self, digital_twin_id: str):
        """ Retrieve a specific digital twin by its ID. """
        try:
            twin = self.client.get_digital_twin(digital_twin_id)
            return twin
        except Exception as e:
            print(f"Error retrieving digital twin {digital_twin_id}: {e}")
            raise

    def query_digital_twins(self, query_expression: str):
        """ Query digital twins using a query expression. """
        try:
            query_result = self.client.query_twins(query_expression)
            return query_result
        except Exception as e:
            print(f"Error querying digital twins: {e}")
            raise

    def delete_digital_twin(self, digital_twin_id: str):
        """ Delete a specific digital twin by its ID. """
        try:
            self.client.delete_digital_twin(digital_twin_id)
            print(f"Digital twin {digital_twin_id} deleted successfully.")
        except Exception as e:
            print(f"Error deleting digital twin {digital_twin_id}: {e}")
            raise

    def update_digital_twin_component(self, digital_twin_id: str, component_name: str, patch: list):
        """ Update a component of a digital twin. """
        try:
            self.client.update_component(digital_twin_id, component_name, patch)
            print(f"Component {component_name} of digital twin {digital_twin_id} updated successfully.")
        except Exception as e:
            print(f"Error updating component {component_name} of digital twin {digital_twin_id}: {e}")
            raise

    def get_digital_twin_component(self, digital_twin_id: str, component_name: str):
        """ Get a component of a digital twin. """
        try:
            component = self.client.get_component(digital_twin_id, component_name)
            return component
        except Exception as e:
            print(f"Error retrieving component {component_name} of digital twin {digital_twin_id}: {e}")
            raise

    def create_relationship(self, source_id: str, relationship_id: str, relationship_data: dict):
        """ Create a relationship between digital twins. """
        try:
            self.client.upsert_relationship(source_id, relationship_id, relationship_data)
            print(f"Relationship {relationship_id} created successfully.")
        except Exception as e:
            print(f"Error creating relationship {relationship_id}: {e}")
            raise

    def list_relationships(self, digital_twin_id: str):
        """ List all relationships for a given digital twin. """
        try:
            relationships = self.client.list_relationships(digital_twin_id)
            return relationships
        except Exception as e:
            print(f"Error listing relationships for digital twin {digital_twin_id}: {e}")
            raise

    def list_incoming_relationships(self, digital_twin_id: str):
        """ List all incoming relationships for a given digital twin. """
        try:
            incoming_relationships = self.client.list_incoming_relationships(digital_twin_id)
            return incoming_relationships
        except Exception as e:
            print(f"Error listing incoming relationships for digital twin {digital_twin_id}: {e}")
            raise

    def create_event_route(self, event_route_id: str, route_data: dict):
        """ Create an event route for the digital twins. """
        try:
            self.client.upsert_event_route(event_route_id, route_data)
            print(f"Event route {event_route_id} created successfully.")
        except Exception as e:
            print(f"Error creating event route {event_route_id}: {e}")
            raise

    def list_event_routes(self):
        """ List all event routes. """
        try:
            event_routes = self.client.list_event_routes()
            return event_routes
        except Exception as e:
            print(f"Error listing event routes: {e}")
            raise

    def delete_event_route(self, event_route_id: str):
        """ Delete an event route by its ID. """
        try:
            self.client.delete_event_route(event_route_id)
            print(f"Event route {event_route_id} deleted successfully.")
        except Exception as e:
            print(f"Error deleting event route {event_route_id}: {e}")
            raise