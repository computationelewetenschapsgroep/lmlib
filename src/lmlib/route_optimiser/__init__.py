from .route_optimizer import compute_optimal_routes, create_default_routing_options, RouteOptimizationModel


from abc import ABC, abstractmethod
from typing import List, Dict


class DataTransformer(ABC):
    """
    An abstract base class for transforming input data for the optimization model.
    """
    
    @abstractmethod
    def transform_data(self, input_data: List[Dict]) -> Dict:
        """
        Transforms the input data into the required format for the optimization model.
        
        :param input_data: The input data to be transformed.
        :return: A dictionary containing the transformed data.
        """
        pass

class OptimizationModel(ABC):
    """
    An abstract base class for solving optimization problems.
    """

    def __init__(self, options: Dict, data_transformer: DataTransformer = None):
        """
        Initialize the optimization model with specific options and an optional data transformer.

        :param options: A dictionary containing options specific to the solver.
        :param data_transformer: An optional instance of a DataTransformer to preprocess input data.
        """
        self.options = options
        self.data_transformer = data_transformer

    @abstractmethod
    def solve(self, input_data: List[Dict]) -> Dict:
        """
        Solve the optimization problem with the given input data.
        
        :param input_data: The input data required for solving the problem.
        :return: The optimized solution as a dictionary.
        """
        pass
