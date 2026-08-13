from lmlib.eta_calculator.cw_planner_client import CWEtaPlannerClient, calculate_cw_eta_plan
from lmlib.schemas.cw_planner import CWEtaPlannerInputPayload, CWVesselInput, CWMonopileInput

class EtaCalculator:
    def __init__(self):
        """
        Initialize the EtaCalculator with data.
        
        """
    def calculate_eta(self):
        """
        Calculate the estimated time of arrival along the trajectory.
        
        :return: The estimated time of arrival as a float.
        """
        return 0.0

__all__ = [
    "EtaCalculator",
    "CWEtaPlannerClient",
    "calculate_cw_eta_plan",
    "CWEtaPlannerInputPayload",
    "CWVesselInput",
    "CWMonopileInput",
]

