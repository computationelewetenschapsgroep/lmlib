from abc import ABC, abstractmethod

from schemas.eta_calculation import MonopileETAResponse

class MonopileETACalculationService(ABC):

    @abstractmethod
    def get_monopile_eta(self) -> MonopileETAResponse:
 
        pass




