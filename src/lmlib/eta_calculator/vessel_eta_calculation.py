from abc import ABC, abstractmethod

from schemas.eta_calculation import VesselETAResponse

class VesselETACalculationService(ABC):

    @abstractmethod
    def get_vessel_eta(self, VesselETARequest) -> VesselETAResponse:
        """
        Fetch ETA information for a specific vessel by its MMSI number (vessel_id).
        
        :param VesselETARequest: contains MMSI number of the vessel
        :return: VesselETAResponse object containing ETA information
        """
        pass
