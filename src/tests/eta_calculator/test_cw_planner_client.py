import unittest
from unittest.mock import MagicMock, patch

from lmlib.eta_calculator.cw_planner_client import CWEtaPlannerClient, calculate_cw_eta_plan
from lmlib.schemas.cw_planner import (
    CWEtaPlannerInputPayload,
    CWMonopileInput,
    CWVesselInput,
)
from lmlib.schemas.model import Monopile, Vessel, VesselType, VesselResponsibility, SpatialDefinition


class TestCWPlannerClient(unittest.TestCase):

    def test_cw_vessel_input_from_dict(self):
        raw_dict = {
            "id": "VESSEL-99",
            "name": "Test Vessel",
            "capacity_weight_tons": 5000.0,
            "max_monopiles": 4,
            "speed_knots": 15.5,
            "available_from_day": 10.0,
            "compatible_grillage_types": ["Type-A", "Type-B"],
            "operational_calendar": "24/7",
            "vessel_class": "TClass",
        }
        vessel = CWVesselInput.from_input(raw_dict)
        self.assertEqual(vessel.id, "VESSEL-99")
        self.assertEqual(vessel.name, "Test Vessel")
        self.assertEqual(vessel.capacity_weight_tons, 5000.0)
        self.assertEqual(vessel.max_monopiles, 4)
        self.assertEqual(vessel.speed_knots, 15.5)

        api_dict = vessel.model_dump(by_alias=True)
        self.assertEqual(api_dict["capacityWeightTons"], 5000.0)
        self.assertEqual(api_dict["maxMonopiles"], 4)
        self.assertEqual(api_dict["speedKnots"], 15.5)
        self.assertEqual(api_dict["compatibleGrillageTypes"], ["Type-A", "Type-B"])

    def test_cw_monopile_input_from_dict(self):
        raw_dict = {
            "id": "MP-99",
            "weight_tons": 1400.0,
            "length_m": 85.0,
            "grillage_type": "Type-B",
            "fabrication_yard_id": "FAB-02",
            "installation_site_id": "SITE-02",
            "fabrication_completion_day": 50.0,
            "target_installation_day": 120.0,
            "origin_logistics_key": "OriginPort",
            "destination_logistics_key": "DestSite",
            "voyage_profile": "DS",
        }
        mp = CWMonopileInput.from_input(raw_dict)
        self.assertEqual(mp.id, "MP-99")
        self.assertEqual(mp.weight_tons, 1400.0)
        self.assertEqual(mp.length_m, 85.0)

        api_dict = mp.model_dump(by_alias=True)
        self.assertEqual(api_dict["weightTons"], 1400.0)
        self.assertEqual(api_dict["lengthM"], 85.0)
        self.assertEqual(api_dict["fabricationYardId"], "FAB-02")

    def test_translation_from_lmlib_models(self):
        spatial = SpatialDefinition(value="POINT(0 0)", format="WKT")
        lmlib_vessel = Vessel(
            ID="V-LMLIB-01",
            vessel_type=VesselType.T_CLASS,
            day_rate=10000.0,
            responsibility=VesselResponsibility.MONOPILE_TRANSPORT,
            spatial_definition=spatial
        )

        lmlib_mp = Monopile(
            id="MP-LMLIB-01",
            name="Monopile 1",
            document_number="DOC-1",
            revision=1,
            phase="1",
            top_mp_flange=10.0,
            bottom_mp_flange=12.0,
            sub_name="Sub",
            dwg_date="2026-01-01",
            site_layout="L1",
            pe_stamp="ST",
            mp_length=90.0,
            glauconite="False",
            punch_through="False",
            design_weight_given=1500.0,
            centre_of_gravity_bottom_of_mp=40.0,
            seabed_level_relative_to_water_depth=20.0,
            spatial_definition=spatial
        )

        payload = CWEtaPlannerInputPayload.from_input({
            "resetBeforeRun": True,
            "vessels": [lmlib_vessel],
            "monopiles": [lmlib_mp]
        })

        api_dict = payload.to_api_dict()
        self.assertTrue(api_dict["resetBeforeRun"])
        self.assertEqual(len(api_dict["vessels"]), 1)
        self.assertEqual(api_dict["vessels"][0]["id"], "V-LMLIB-01")
        self.assertEqual(len(api_dict["monopiles"]), 1)
        self.assertEqual(api_dict["monopiles"][0]["id"], "MP-LMLIB-01")
        self.assertEqual(api_dict["monopiles"][0]["weightTons"], 1500.0)
        self.assertEqual(api_dict["monopiles"][0]["lengthM"], 90.0)

    @patch("requests.get")
    def test_client_check_status(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "status": "UP",
            "service": "CW ETA Planner API",
            "endpoints": {"solver_run": "/api/v1/solver/run"}
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        client = CWEtaPlannerClient(base_url="http://localhost:8080")
        status = client.check_status()

        self.assertEqual(status["status"], "UP")
        mock_get.assert_called_once_with("http://localhost:8080/api/v1/status", timeout=60.0)

    @patch("requests.get")
    def test_client_get_parameters(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {"parameters": ["resetBeforeRun", "tripCount"]}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        client = CWEtaPlannerClient(base_url="http://localhost:8080")
        params = client.get_parameters()

        self.assertIn("parameters", params)
        mock_get.assert_called_once_with("http://localhost:8080/api/v1/solver/parameters", timeout=60.0)

    @patch("requests.post")
    def test_client_run_solver(self, mock_post):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "bestSolverName": "Simulated Annealing",
            "bestScore": "0hard/120soft",
            "schedule": {"trips": [{"tripId": 1}, {"tripId": 2}]}
        }
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        client = CWEtaPlannerClient()
        result = client.run_solver({"tripCount": 2})

        self.assertEqual(result["bestSolverName"], "Simulated Annealing")
        self.assertEqual(len(result["schedule"]["trips"]), 2)
        mock_post.assert_called_once()
        call_args = mock_post.call_args
        self.assertEqual(call_args[0][0], "http://localhost:8080/api/v1/solver/run")
        self.assertEqual(call_args[1]["json"]["tripCount"], 2)

    @patch("requests.post")
    def test_client_reset_scenarios(self, mock_post):
        mock_response = MagicMock()
        mock_response.json.return_value = {"status": "RESET_SUCCESS"}
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        client = CWEtaPlannerClient()
        res = client.reset_scenarios()

        self.assertEqual(res["status"], "RESET_SUCCESS")
        mock_post.assert_called_once_with("http://localhost:8080/api/v1/scenarios/reset", json={}, headers={"Content-Type": "application/json"}, timeout=60.0)

    @patch("requests.get")
    def test_client_download_pdf_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b"%PDF-1.4 dummy content"
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        client = CWEtaPlannerClient()
        pdf_bytes = client.download_report_pdf(output_filename="")

        self.assertEqual(pdf_bytes, b"%PDF-1.4 dummy content")

    @patch("requests.get")
    def test_client_download_pdf_not_found(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        client = CWEtaPlannerClient()
        pdf_bytes = client.download_report_pdf(output_filename="")

        self.assertIsNone(pdf_bytes)

    @patch("requests.get")
    @patch("requests.post")
    def test_calculate_cw_eta_plan_convenience_fn(self, mock_post, mock_get):
        mock_status_res = MagicMock()
        mock_status_res.json.return_value = {"status": "UP"}
        mock_status_res.raise_for_status.return_value = None
        mock_get.return_value = mock_status_res

        mock_run_res = MagicMock()
        mock_run_res.json.return_value = {"bestSolverName": "Hill Climbing", "bestScore": "0hard/50soft"}
        mock_run_res.raise_for_status.return_value = None
        mock_post.return_value = mock_run_res

        res = calculate_cw_eta_plan(input_data={"tripCount": 3})
        self.assertEqual(res["bestSolverName"], "Hill Climbing")


if __name__ == "__main__":
    unittest.main()
