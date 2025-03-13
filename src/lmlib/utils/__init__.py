def validate_wkt(wkt: str) -> str:
    # validate if the location is a valid WKT format
    if not wkt.startswith("POINT"):
        raise ValueError(f"Invalid WKT format: {wkt}")
    return wkt