
from src.lmlib.schemas.model import Port, SpatialDefinition, Vessel, VesselType, Monopile, FabricationYard

port = Port(spatial_definition=SpatialDefinition(value="Port1", format="JSON", SRID=4326, description="Main Port"))

vessel1 = Vessel(vessel_type=VesselType.ATLAS, day_rate=10000, responsibility="Transport", port=port, fabrication_yard=None, wind_farm=None)
vessel2 = Vessel(vessel_type=VesselType.SYMPHONY, day_rate=20000, responsibility="Transport", port=port, fabrication_yard=None, wind_farm=None)

monopile1 = Monopile(name="MP001", document_number="12345", revision=1, phase="Installation", top_mp_flange=10.5, bottom_mp_flange=12.5,
                     id="MP001", sub_name="Sub1", dwg_date="2025-02-01", site_layout="Layout1", pe_stamp="PE123",
                     mp_length=40.0, glauconite="Yes", punch_through="No", design_weight_given=100000,
                     centre_of_gravity_bottom_of_mp=5.0, seabed_level_relative_to_water_depth=15.0, spatial_definition=SpatialDefinition(value="Monopile1", format="JSON", SRID=4326))

monopile2 = Monopile(name="MP002", document_number="12346", revision=1, phase="Installation", top_mp_flange=10.5, bottom_mp_flange=12.5,
                     id="MP002", sub_name="Sub2", dwg_date="2025-03-01", site_layout="Layout2", pe_stamp="PE124",
                     mp_length=42.0, glauconite="Yes", punch_through="Yes", design_weight_given=120000,
                     centre_of_gravity_bottom_of_mp=6.0, seabed_level_relative_to_water_depth=16.0, spatial_definition=SpatialDefinition(value="Monopile2", format="JSON", SRID=4326))

fabrication_yard = FabricationYard(spatial_definition=SpatialDefinition(value="Yard1", format="JSON", SRID=4326), monopiles=[monopile1, monopile2])

stops_data = [
    {"id": "P001", "location": {"lon": -53.987533, "lat": 47.291122}, "demand": 0, "duration": 18000, "quantity": 0},
    {"id": "F001", "location": {"lon": -9.27148, "lat": 41.9296}, "demand": 300, "duration": 43200.0, "quantity": 0, "succeeds": "P001",  "unplanned_penalty": 500000},
    {"id": "M001", "location": {"lon": -62.503349, "lat": 44.518828}, "demand": 500, "duration": 70200.0, "quantity": 0, "succeeds": "F001",  "unplanned_penalty": 500000},
    {"id": "OF001", "location": {"lon": -75.59966, "lat": 34.937392}, "demand": 180, "duration": 0, "quantity": 0, "succeeds": "F001",  "unplanned_penalty": 500000, "target_arrival_time": "2025-03-25T00:00:00-00:00"},
]

vessels_data = [
   {'id': 'ATLAS', 'start_location': {'lon': -19.8178032, 'lat': 34.937392}, 'end_location': {'lon': -75.59966, 'lat': 34.937392}, 'start_time': '2025-02-25T00:00:00-00:00', 'end_time': '2025-03-25T00:00:00-00:00', 'capacity': 5},
   {'id': 'SYMPHONY', 'start_location': {'lon': -62.5415968, 'lat': 62.1273427}, 'end_location': {'lon': -75.59966, 'lat': 34.937392}, 'start_time': '2025-03-01T00:00:00-00:00', 'end_time': '2025-03-25T00:00:00-00:00', 'capacity': 1} 
]

final_combined_data = {
    "defaults": {
        "vehicles": {
            "speed": 34.44
        },
    },
    "stops": stops_data,
    "vehicles": vessels_data
}


from src.lmlib.route_optimiser.nextmv import NextmvDataTransformer

data_transformer = NextmvDataTransformer()

transformed_data = data_transformer.transform_data(final_combined_data)

import nextmv
options = nextmv.Options() 

from src.lmlib.route_optimiser.nextmv import MaritimeRouteOptimizationModel

optimization_model = MaritimeRouteOptimizationModel(nextmv.Options(), 
                                                    NextmvDataTransformer().transform_data(final_combined_data))

result = optimization_model.solve(transformed_data)

# Output the result
print("Optimal routes:")
print(result)

