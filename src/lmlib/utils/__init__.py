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