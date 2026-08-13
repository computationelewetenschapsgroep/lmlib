import logging
from typing import Any, Dict, Optional, Union
import requests

from lmlib.schemas.cw_planner import (
    CWEtaPlannerInputPayload,
    CWPlannerRunResponse,
    CWPlannerStatusResponse,
)

logger = logging.getLogger(__name__)


class CWEtaPlannerClient:
    """
    Client service for interacting with the CW ETA Planner REST API.
    
    Translates lmlib inputs or dictionary payloads into the format expected by the
    CW ETA Planner API and communicates with the endpoints.
    """

    def __init__(
        self,
        base_url: str = "http://localhost:8080",
        base_path: str = "/api/v1",
        timeout: float = 60.0,
    ):
        """
        Initialize the CWEtaPlannerClient.

        :param base_url: Host base URL (e.g. http://localhost:8080)
        :param base_path: API version prefix (e.g. /api/v1)
        :param timeout: Request timeout in seconds
        """
        base_url_clean = base_url.rstrip("/")
        base_path_clean = "/" + base_path.strip("/")
        self.api_url = f"{base_url_clean}{base_path_clean}"
        self.timeout = timeout

    def check_status(self) -> Dict[str, Any]:
        """
        Check service health & endpoint listing (GET /api/v1/status).
        """
        url = f"{self.api_url}/status"
        res = requests.get(url, timeout=self.timeout)
        res.raise_for_status()
        data = res.json()
        logger.info(f"CW ETA Planner Status: {data.get('status')}")
        return data

    def get_parameters(self) -> Dict[str, Any]:
        """
        Get structured documentation of all accepted input parameters (GET /api/v1/solver/parameters).
        """
        url = f"{self.api_url}/solver/parameters"
        res = requests.get(url, timeout=self.timeout)
        res.raise_for_status()
        return res.json()

    def translate_input(
        self, input_data: Optional[Union[Dict[str, Any], CWEtaPlannerInputPayload, Any]] = None
    ) -> Dict[str, Any]:
        """
        Translate high-level input (dict, CWEtaPlannerInputPayload, or lmlib domain models)
        into the JSON structure required by CW ETA Planner API.
        """
        payload_model = CWEtaPlannerInputPayload.from_input(input_data)
        return payload_model.to_api_dict()

    def run_solver(
        self, input_data: Optional[Union[Dict[str, Any], CWEtaPlannerInputPayload, Any]] = None
    ) -> Dict[str, Any]:
        """
        Runs solver optimization pipeline (Hill Climbing -> Tabu Search -> Simulated Annealing).
        (POST /api/v1/solver/run)

        :param input_data: Optional input payload, lmlib objects, or None to use digital twin defaults
        :return: JSON object containing solver results (bestSolverName, bestScore, schedule, etc.)
        """
        payload = self.translate_input(input_data)
        url = f"{self.api_url}/solver/run"
        headers = {"Content-Type": "application/json"}

        logger.info(f"Posting request to CW ETA Planner solver at {url}")
        res = requests.post(url, json=payload, headers=headers, timeout=self.timeout)
        res.raise_for_status()

        data = res.json()
        logger.info(
            f"Solver execution complete. Best Solver: {data.get('bestSolverName')}, Score: {data.get('bestScore')}"
        )
        return data

    def reset_scenarios(self, custom_payload: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Resets cached solver results (POST /api/v1/scenarios/reset).
        """
        payload = custom_payload if custom_payload is not None else {}
        url = f"{self.api_url}/scenarios/reset"
        headers = {"Content-Type": "application/json"}

        res = requests.post(url, json=payload, headers=headers, timeout=self.timeout)
        res.raise_for_status()
        return res.json()

    def download_report_pdf(
        self, output_filename: str = "schedule_report.pdf"
    ) -> Optional[bytes]:
        """
        Downloads the last optimized schedule as a PDF report (GET /api/v1/solver/report/pdf).

        :param output_filename: Path to save the downloaded PDF report file
        :return: Raw PDF byte content if available, None if 404 (not run yet)
        """
        url = f"{self.api_url}/solver/report/pdf"
        res = requests.get(url, timeout=self.timeout)
        if res.status_code == 404:
            logger.warning("No PDF report available from CW ETA Planner (404). Run solver first.")
            return None
        res.raise_for_status()

        if output_filename:
            with open(output_filename, "wb") as f:
                f.write(res.content)
            logger.info(f"PDF report saved as {output_filename}")

        return res.content


def calculate_cw_eta_plan(
    input_data: Optional[Union[Dict[str, Any], CWEtaPlannerInputPayload, Any]] = None,
    base_url: str = "http://localhost:8080",
    output_pdf_filename: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Convenience function to translate input, run CW ETA Planner solver, and optionally download PDF report.

    :param input_data: Input parameters/models or None for default digital twin scenario
    :param base_url: Base URL of CW ETA Planner service
    :param output_pdf_filename: Optional filename to save PDF schedule report
    :return: Dict containing solver execution results
    """
    client = CWEtaPlannerClient(base_url=base_url)
    client.check_status()
    result = client.run_solver(input_data=input_data)

    if output_pdf_filename:
        client.download_report_pdf(output_filename=output_pdf_filename)

    return result
