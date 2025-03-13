from abc import ABC, abstractmethod
from schemas.process_twin import (
    ActivityPutRequest,
    ActivityPutResponse,
    ActivityGetRequest,
    ActivityGetResponse,
)

class TwinProcessingService(ABC):

    @abstractmethod
    def update_activity(self, request: ActivityPutRequest) -> ActivityPutResponse:
        """
        Update or create an activity associated with a digital twin. The activity details such as name, start/end date, and cost 
        will be updated or created based on the provided data.
        
        :param request: Contains activity details to be updated or created.
        :return: A response with the twin ID of the created or updated activity.
        """
        pass

    @abstractmethod
    def get_activity(self, request: ActivityGetRequest) -> ActivityGetResponse:
        """
        Fetch the details of an activity by its unique activity ID. This will provide information about the activity's 
        name, start/end dates, cost, and associated digital twin ID.
        
        :param request: Contains the activity ID for which details are to be fetched.
        :return: The details of the activity, including the twin ID.
        """
        pass
