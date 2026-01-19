# from lmlib.route_optimiser import compute_optimal_routes, create_default_routing_options, RouteOptimizationModel



# vehicle_capacity = {
#     "bunnies": 20,
#     "rabbits": 10
# }

# vehicle_start_end_location = {
#     "start_location": {
#         "lat": 35.791729813680874,
#         "lon": -78.7401685145487
#     },
#     "end_location": {
#         "lat": 35.791729813680874,
#         "lon": -78.7401685145487
#     }
# }

# vehicle_speed = 34.44

# #Stop Information
# stop_default = {
#     # "duration": 300,
#     # "quantity": {
#     #     "bunnies": -1,
#     #     "rabbits": -1
#     # },
#     # "unplanned_penalty": 200000,
#     # "target_arrival_time": "2023-01-01T10:00:00Z",
#     "early_arrival_time_penalty": 1.5,
#     "late_arrival_time_penalty": 1.5
# }

# # List of all stops
# stops_data = [
#     {"id": "P001", "location": {"lon": -53.987533, "lat": 47.291122}, "demand": 0, "duration": 18000, "quantity": 0},
#     {"id": "F001", "location": {"lon": -9.27148, "lat": 41.9296}, "demand": 300, "duration": 43200.0, "quantity": 0, "succeeds": "P001",  "unplanned_penalty": 500000},
#     {"id": "M001", "location": {"lon": -62.503349, "lat": 44.518828}, "demand": 500, "duration": 70200.0, "quantity": 0, "succeeds": "F001",  "unplanned_penalty": 500000},
#     {"id": "OF001", "location": {"lon": -75.59966, "lat": 34.937392}, "demand": 180, "duration": 0, "quantity": 0, "succeeds": "F001",  "unplanned_penalty": 500000, "target_arrival_time": "2025-03-25T00:00:00-00:00"},
# ]

# # Vehicle Information
# vehicles_data = [
#    {'id': 'ATLAS', 'start_location': {'lon': -19.8178032, 'lat': 34.937392},'end_location': {'lon': -75.59966, 'lat': 34.937392}, 'start_time': '2025-02-25T00:00:00-00:00', 'end_time': '2025-03-25T00:00:00-00:00', 'capacity': 5},
#    {'id': 'BOKALIFT', 'start_location': {'lon': -62.5415968, 'lat': 62.1273427},'end_location': {'lon': -75.59966, 'lat': 34.937392} ,'start_time': '2025-03-01T00:00:00-00:00', 'end_time': '2025-03-25T00:00:00-00:00', 'capacity': 1} 
# ]

# # final structure
# final_combined_data = {
#     "defaults": {
#         "vehicles": {
#             # "capacity": vehicle_capacity,
#             # "start_end_location": vehicle_start_end_location,
#             "speed": vehicle_speed
#         },
#         #"stops": stop_default
#     },
#     "stops": stops_data,
#     "vehicles": vehicles_data
# }

# # print(final_combined_data)
# options = create_default_routing_options()

# print(options) # this is of type- <nextmv.options.Options object at 0x1049c3070>

# #print the value of options
# print(options["solver_options"]) # this is of type- <nextmv.options.Options object at 0x1049c3070>

# # Solve the problem
# # result = compute_optimal_routes(final_combined_data, options)

# # # print(result.keys())
# # # print(result["solution"])
# # print(result)


from lmlib.azure_digital_twin.adt_service import AzureDigitalTwinsService
from azure.identity import DefaultAzureCredential
from lmlib.schemas.model import (Decklength, FabricationYard, GrillageType,
                                 Monopile)
from lmlib.eta_calculator.deterministic.monopile.length_configuration import LengthConfigurations

adt_service = AzureDigitalTwinsService(
    adt_endpoint = "https://owf-adt.api.neu.digitaltwins.azure.net", 
    credential = DefaultAzureCredential()
)

length_config = LengthConfigurations(
    adt_service,
    "LengthCompatibility",
    Monopile,
    "mpLength",
    Decklength,
    "value",
    True,
)

for monopile, deck_length in length_config.get():
    print(f"MP - {monopile.mp_length} and Decklength - {deck_length.value}")