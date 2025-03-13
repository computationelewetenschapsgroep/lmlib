from abc import ABC, abstractmethod
from schemas.asset_twin import (
    VesselGetRequest,
    VesselGetResponse,
    VesselPutRequest,
    VesselPutResponse,
    VesselDeleteRequest,
    VesselDeleteResponse,
    VesselGetListRequest,
    VesselGetListResponse,
    MonopileGetRequest,
    MonopileGetResponse,
    MonopilePutRequest,
    MonopilePutResponse,
    MonopileDeleteRequest,
    MonopileDeleteResponse,
    MonopileGetListRequest,
    MonopileGetListResponse,
    PortGetRequest,
    PortGetResponse,
    PortPutRequest,
    PortPutResponse,
    PortDeleteRequest,
    PortDeleteResponse,
    PortGetListRequest,
    PortGetListResponse,
    ConnectionPutRequest,
    ConnectionPutResponse,
    RelationGetRequest,
    RelationGetResponse,
    RelationDeleteRequest,
)

class AssetTwinService(ABC):

    @abstractmethod
    def get_vessel(self, request: VesselGetRequest) -> VesselGetResponse:
        """
        Fetch the asset details of a vessel based on its MMSI number.
        
        :param request: The vessel_id (MMSI number) for which details are to be fetched.
        :return: The details of the vessel, including its twin ID and location.
        """
        pass

    @abstractmethod
    def update_vessel(self, request: VesselPutRequest) -> VesselPutResponse:
        """
        Update the vessel details such as name, location, and responsibility.
        
        :param request: The vessel details to be updated.
        :return: A response with the twin ID of the updated vessel.
        """
        pass

    @abstractmethod
    def delete_vessel(self, request: VesselDeleteRequest) -> VesselDeleteResponse:
        """
        Delete a vessel based on its MMSI number.
        
        :param request: The vessel ID (MMSI number) to delete.
        :return: A response containing the twin ID of the deleted vessel.
        """
        pass

    @abstractmethod
    def get_vessels(self, request: VesselGetListRequest) -> VesselGetListResponse:
        """
        Fetch a list of vessels with pagination support.
        
        :param request: Limit the number of vessels to return.
        :return: A list of vessels with their details.
        """
        pass

    @abstractmethod
    def get_monopile(self, request: MonopileGetRequest) -> MonopileGetResponse:
        """
        Fetch the asset details of a monopile based on its identifier.
        
        :param request: The monopile_id to fetch.
        :return: The details of the monopile, including twin ID and location.
        """
        pass

    @abstractmethod
    def update_monopile(self, request: MonopilePutRequest) -> MonopilePutResponse:
        """
        Update the monopile details such as location and status.
        
        :param request: The monopile details to be updated.
        :return: A response with the twin ID of the updated monopile.
        """
        pass

    @abstractmethod
    def delete_monopile(self, request: MonopileDeleteRequest) -> MonopileDeleteResponse:
        """
        Delete a monopile based on its identifier.
        
        :param request: The monopile ID to delete.
        :return: A response containing the twin ID of the deleted monopile.
        """
        pass

    @abstractmethod
    def get_monopiles(self, request: MonopileGetListRequest) -> MonopileGetListResponse:
        """
        Fetch a list of monopiles with pagination support.
        
        :param request: Limit the number of monopiles to return.
        :return: A list of monopiles with their details.
        """
        pass

    @abstractmethod
    def get_port(self, request: PortGetRequest) -> PortGetResponse:
        """
        Fetch the asset details of a port based on its identifier.
        
        :param request: The port ID to fetch.
        :return: The details of the port, including twin ID, name, and location.
        """
        pass

    @abstractmethod
    def update_port(self, request: PortPutRequest) -> PortPutResponse:
        """
        Update the port details such as name, location, and role.
        
        :param request: The port details to be updated.
        :return: A response with the twin ID of the updated port.
        """
        pass

    @abstractmethod
    def delete_port(self, request: PortDeleteRequest) -> PortDeleteResponse:
        """
        Delete a port based on its identifier.
        
        :param request: The port ID to delete.
        :return: A response containing the twin ID of the deleted port.
        """
        pass

    @abstractmethod
    def get_ports(self, request: PortGetListRequest) -> PortGetListResponse:
        """
        Fetch a list of ports with pagination support.
        
        :param request: Limit the number of ports to return.
        :return: A list of ports with their details.
        """
        pass

    @abstractmethod
    def connect_assets(self, request: ConnectionPutRequest) -> ConnectionPutResponse:
        """
        Create a relationship between two asset twins.
        
        :param request: The connection details including source and target twin IDs.
        :return: A response with the twin ID of the created relationship.
        """
        pass

    @abstractmethod
    def get_relations(self, request: RelationGetRequest) -> RelationGetResponse:
        """
        Fetch all relationships associated with a particular twin ID.
        
        :param request: The twin ID to get relationships for.
        :return: A list of relationships for the given twin ID.
        """
        pass

    @abstractmethod
    def delete_relation(self, request: RelationDeleteRequest) -> None:
        """
        Delete a specific relationship between twin assets.
        
        :param request: The relation ID to delete.
        :return: None
        """
        pass