from typing import List, Dict
import nextmv
from lmlib.route_optimiser import DataTransformer, OptimizationModel

class NextmvDataTransformer(DataTransformer):

    def transform_data(self, input_data: List[Dict]) -> Dict:
        """
        Transforms the input data into the format required for Nextmv's VRP solver.
        """
        stops_data = input_data.get("stops", [])
        vehicles_data = input_data.get("vehicles", [])
        defaults = input_data.get("defaults", {})

        stops = []
        for stop in stops_data:
            stops.append({
                "id": stop["id"],
                "location": stop["location"],
                "demand": stop["demand"],
                "duration": stop["duration"],
                "quantity": stop["quantity"],
                "succeeds": stop.get("succeeds", None),
                "unplanned_penalty": stop.get("unplanned_penalty", 0),
                "target_arrival_time": stop.get("target_arrival_time", None)
            })

        vehicles = []
        for vehicle in vehicles_data:
            vehicles.append({
                "id": vehicle["id"],
                "start_location": vehicle["start_location"],
                "end_location": vehicle["end_location"],
                "start_time": vehicle["start_time"],
                "end_time": vehicle["end_time"],
                "capacity": vehicle["capacity"]
            })

        defaults_data = defaults.get("vehicles", {})
        vehicle_speed = defaults_data.get("speed", 34.44)

        transformed_data = {
            "defaults": {
                "vehicles": {
                    "speed": vehicle_speed
                }
            },
            "stops": stops,
            "vehicles": vehicles
        }

        return transformed_data



class MaritimeRouteOptimizationModel(OptimizationModel):

    def __init__(self, options: nextmv.Options, data_transformer: DataTransformer = None):
        super().__init__(options, data_transformer)

    def solve(self, input_data: List[Dict]) -> Dict:
        nextroute_input = nextmv.schema.Input.from_dict(input_data)
        nextroute_options = nextmv.Options.extract_from_dict(self.options.to_dict())

        nextroute_output = nextmv.solve(nextroute_input, nextroute_options)

        return {
            "solution": nextroute_output.solutions[0].to_dict(),
            "statistics": nextroute_output.statistics.to_dict()
        }
