import nextroute
import nextmv
from typing import List


class RouteOptimizationModel(nextmv.Model):
    def __init__(self, options: nextmv.Options):
        """
        Initialize the RouteOptimizationModel with a given set of options.
        """
        self.options = options

    def solve(self, input_data: List[dict]) -> dict:
        """
        Solves the given Vehicle Routing Problem (VRP) and returns the optimized routes.

        Parameters:
        - input_data: List of dicts formatted in the same way as nextroute.schema.Input.

        Returns:
        - dict: Optimized routing solution.
        """
        # Convert input data into the format needed by nextroute
        nextroute_input = nextroute.schema.Input.from_dict(input_data)
        nextroute_options = nextroute.Options.extract_from_dict(self.options.to_dict())

        # Solve the problem using nextroute to get optimal routes
        nextroute_output = nextroute.solve(nextroute_input, nextroute_options)

        # Prepare and return the solution, including routing details and statistics
        return {
            "solution": nextroute_output.solutions[0].to_dict(),
            "statistics": nextroute_output.statistics.to_dict()
        }


def create_default_routing_options() -> nextmv.Options:
    """
    Create default options for the Vehicle Routing Problem (VRP) solver.

    Returns:
    - nextmv.Options: Default options object for route optimization.
    """
    parameters = []

    # Get the default options from nextroute
    default_options = nextroute.Options()
    for name, default_value in default_options.to_dict().items():
        parameters.append(nextmv.Parameter(name.lower(), type(default_value), default_value, name, False))

    return nextmv.Options(*parameters)


def compute_optimal_routes(input_data: List[dict], options: nextmv.Options) -> dict:
    """
    A convenience function to compute the optimal routes for the given VRP input data.

    Parameters:
    - input_data: List of dicts, the input data in the format expected by nextroute.
    - options: nextmv.Options, the options to be used for solving the VRP.

    Returns:
    - dict: The optimized solution for the routing problem.
    """
    model = RouteOptimizationModel(options)
    return model.solve(input_data)

