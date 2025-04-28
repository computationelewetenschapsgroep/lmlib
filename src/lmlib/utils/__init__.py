import inspect
from typing import Any
from pydantic import BaseModel

def validate_wkt(wkt: str) -> str:
    # validate if the location is a valid WKT format
    if not wkt.startswith("POINT"):
        raise ValueError(f"Invalid WKT format: {wkt}")
    return wkt

def singleton(cls):
    """ A decorator to ensure that only one instance of the class is created. """
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance

def is_model_defined_with_model_id(
    module: Any, model_name: str, check_subclass_of_basemodel: bool = False
) -> bool:
    if not inspect.ismodule(module):
        raise ValueError("The provided argument is not a valid module.")
    
    model = getattr(module, model_name, None)
    
    if model:
        if hasattr(model, 'model_fields') and 'model_id' in model.model_fields:
            if check_subclass_of_basemodel and not issubclass(model, BaseModel):
                return False
            return True
    
    return False