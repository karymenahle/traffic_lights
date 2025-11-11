from dataclasses import dataclass

@dataclass
class ArrivalConfig:
    lam_N: float = 0.6
    lam_E: float = 0.6
    lam_S: float = 0.6
    lam_W: float = 0.6

@dataclass
class PhaseConfig:
    min_green: int = 10
    amber: int = 3
    all_red: int = 1
    saturation_flow: int = 2  # cars per tick per green approach

@dataclass
class SimConfig:
    horizon: int = 1200  # seconds per run
    seed: int = 7
    dt: int = 1
