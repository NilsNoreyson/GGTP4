from dataclasses import dataclass

@dataclass
class CityPipe:
    pipe_id: int
    material: str
    diameter: float
    length: float
    start_coordinates: Tuple[float, float]
    end_coordinates: Tuple[float, float]
