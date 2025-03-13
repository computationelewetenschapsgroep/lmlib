import pytest
import nextroute
import nextmv
from lmlib.route_optimiser import RouteOptimizationModel, compute_optimal_routes, create_default_routing_options
from unittest.mock import MagicMock

input_data = {
    "defaults": {"vehicles": {"speed": 34.44}},
    "stops": [
        {
            "id": "P001",
            "location": {"lon": -53.987533, "lat": 47.291122},
            "demand": 0,
            "duration": 18000,
            "quantity": 0,
        },
        {
            "id": "F001",
            "location": {"lon": -9.27148, "lat": 41.9296},
            "demand": 300,
            "duration": 43200.0,
            "quantity": 0,
            "succeeds": "P001",
            "unplanned_penalty": 500000,
        },
        {
            "id": "M001",
            "location": {"lon": -62.503349, "lat": 44.518828},
            "demand": 500,
            "duration": 70200.0,
            "quantity": 0,
            "succeeds": "F001",
            "unplanned_penalty": 500000,
        },
        {
            "id": "OF001",
            "location": {"lon": -75.59966, "lat": 34.937392},
            "demand": 180,
            "duration": 0,
            "quantity": 0,
            "succeeds": "F001",
            "unplanned_penalty": 500000,
            "target_arrival_time": "2025-03-25T00:00:00-00:00",
        },
    ],
    "vehicles": [
        {
            "id": "ATLAS",
            "start_location": {"lon": -19.8178032, "lat": 34.937392},
            "end_location": {"lon": -75.59966, "lat": 34.937392},
            "start_time": "2025-02-25T00:00:00-00:00",
            "end_time": "2025-03-25T00:00:00-00:00",
            "capacity": 5,
        },
        {
            "id": "BOKALIFT",
            "start_location": {"lon": -62.5415968, "lat": 62.1273427},
            "end_location": {"lon": -75.59966, "lat": 34.937392},
            "start_time": "2025-03-01T00:00:00-00:00",
            "end_time": "2025-03-25T00:00:00-00:00",
            "capacity": 1,
        },
    ],
}

expected_output = {
    "solution": {
        "unplanned": [],
        "vehicles": [
            {
                "id": "ATLAS",
                "route": [
                    {
                        "stop": {
                            "id": "ATLAS-start",
                            "location": {"lat": 34.937392, "lon": -19.8178032},
                        },
                        "arrival_time": "2025-02-25T00:00:00Z",
                        "cumulative_travel_duration": 0.0,
                        "end_time": "2025-02-25T00:00:00Z",
                        "start_time": "2025-02-25T00:00:00Z",
                        "travel_duration": 0.0,
                    },
                    {
                        "stop": {
                            "id": "P001",
                            "location": {"lat": 47.291122, "lon": -53.987533},
                        },
                        "arrival_time": "2025-02-26T01:20:21Z",
                        "cumulative_travel_distance": 3141652.0,
                        "cumulative_travel_duration": 91221.0,
                        "duration": 18000.0,
                        "end_time": "2025-02-26T06:20:21Z",
                        "start_time": "2025-02-26T01:20:21Z",
                        "travel_distance": 3141652.0,
                        "travel_duration": 91221.0,
                    },
                    {
                        "stop": {
                            "id": "F001",
                            "location": {"lat": 41.9296, "lon": -9.27148},
                        },
                        "arrival_time": "2025-02-27T10:53:18Z",
                        "cumulative_travel_distance": 6681293.0,
                        "cumulative_travel_duration": 193998.0,
                        "duration": 43200.0,
                        "end_time": "2025-02-27T22:53:18Z",
                        "start_time": "2025-02-27T10:53:18Z",
                        "travel_distance": 3539641.0,
                        "travel_duration": 102777.0,
                    },
                    {
                        "stop": {
                            "id": "M001",
                            "location": {"lat": 44.518828, "lon": -62.503349},
                        },
                        "arrival_time": "2025-03-01T09:07:58Z",
                        "cumulative_travel_distance": 10927056.0,
                        "cumulative_travel_duration": 317278.0,
                        "duration": 70200.0,
                        "end_time": "2025-03-02T04:37:58Z",
                        "start_time": "2025-03-01T09:07:58Z",
                        "travel_distance": 4245763.0,
                        "travel_duration": 123280.0,
                    },
                    {
                        "stop": {
                            "id": "OF001",
                            "location": {"lat": 34.937392, "lon": -75.59966},
                        },
                        "arrival_time": "2025-03-02T17:04:15Z",
                        "cumulative_travel_distance": 12469199.0,
                        "cumulative_travel_duration": 362055.0,
                        "end_time": "2025-03-02T17:04:15Z",
                        "start_time": "2025-03-02T17:04:15Z",
                        "target_arrival_time": "2025-03-25T00:00:00Z",
                        "travel_distance": 1542143.0,
                        "travel_duration": 44777.0,
                    },
                    {
                        "stop": {
                            "id": "ATLAS-end",
                            "location": {"lat": 34.937392, "lon": -75.59966},
                        },
                        "arrival_time": "2025-03-02T17:04:15Z",
                        "cumulative_travel_distance": 12469199.0,
                        "cumulative_travel_duration": 362055.0,
                        "end_time": "2025-03-02T17:04:15Z",
                        "start_time": "2025-03-02T17:04:15Z",
                        "travel_duration": 0.0,
                    },
                ],
                "route_duration": 493455.0,
                "route_stops_duration": 131400.0,
                "route_travel_distance": 12469199.0,
                "route_travel_duration": 362055.0,
            },
            {
                "id": "BOKALIFT",
                "route": [
                    {
                        "stop": {
                            "id": "BOKALIFT-start",
                            "location": {"lat": 62.1273427, "lon": -62.5415968},
                        },
                        "arrival_time": "2025-03-01T00:00:00Z",
                        "cumulative_travel_duration": 0.0,
                        "end_time": "2025-03-01T00:00:00Z",
                        "start_time": "2025-03-01T00:00:00Z",
                        "travel_duration": 0.0,
                    },
                    {
                        "stop": {
                            "id": "BOKALIFT-end",
                            "location": {"lat": 34.937392, "lon": -75.59966},
                        },
                        "arrival_time": "2025-03-02T01:28:38Z",
                        "cumulative_travel_distance": 3158770.0,
                        "cumulative_travel_duration": 91718.0,
                        "end_time": "2025-03-02T01:28:38Z",
                        "start_time": "2025-03-02T01:28:38Z",
                        "travel_distance": 3158770.0,
                        "travel_duration": 91718.0,
                    },
                ],
                "route_duration": 91718.0,
                "route_travel_distance": 3158770.0,
                "route_travel_duration": 91718.0,
            },
        ],
        "objective": {
            "name": "1 * vehicles_duration + 1 * unplanned_penalty",
            "objectives": [
                {
                    "name": "vehicles_duration",
                    "factor": 1,
                    "base": 585173.8695342541,
                    "value": 585173.8695342541,
                },
                {"name": "unplanned_penalty", "factor": 1, "value": 0},
            ],
            "value": 585173.8695342541,
        },
    },
    "statistics": {
        "run": {"duration": 5.000183875, "iterations": 1530151},
        "result": {
            "duration": 0.0060085,
            "value": 585173.8695342541,
            "custom": {
                "activated_vehicles": 1,
                "unplanned_stops": 0,
                "max_travel_duration": 362055,
                "max_duration": 493455,
                "min_travel_duration": 362055,
                "min_duration": 493455,
                "max_stops_in_vehicle": 4,
                "min_stops_in_vehicle": 4,
            },
        },
        "series_data": {
            "value": {
                "name": "1 * vehicles_duration + 1 * unplanned_penalty",
                "data_points": [{"x": 0.0060085, "y": 585173.8695342541}],
            },
            "custom": [
                {"name": "iterations", "data_points": [{"x": 0.0060085, "y": 0.0}]}
            ],
        },
        "schema": "v1",
    },
}

@pytest.fixture
def mock_nextroute_solve(mocker):
    return mocker.patch("nextroute.solve")


def test_route_optimization(mock_nextroute_solve):
    mock_solution = MagicMock()
    mock_solution.solutions = [MagicMock(to_dict=MagicMock(return_value=expected_output["solution"]))]
    mock_solution.statistics = MagicMock(to_dict=MagicMock(return_value=expected_output["statistics"]))
    
    mock_nextroute_solve.return_value = mock_solution

    mock_options = MagicMock(spec=nextmv.Options)

    model = RouteOptimizationModel(mock_options)

    result = model.solve(input_data)

    mock_nextroute_solve.assert_called_once()

    assert "solution" in result
    assert result["solution"] == expected_output["solution"]

    assert "statistics" in result
    assert result["statistics"] == expected_output["statistics"]