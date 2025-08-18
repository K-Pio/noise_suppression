from dataclasses import dataclass
from typing import List, Tuple
from audio import SoundSourceBase

Vec2 = Tuple[float, float]

@dataclass
class Obstacle:
    a: Vec2
    b: Vec2
    absorb: float  # 0..1

@dataclass
class SoundSource:
    pos: Vec2
    # freq: float
    # base_gain: float = 1.0
    # r0: float = 50.0
    # rmax: float = 400.0
    generator: SoundSourceBase

@dataclass
class Listener:
    pos: Vec2

@dataclass
class Map2D:
    size: int
    obstacles: List[Obstacle]
