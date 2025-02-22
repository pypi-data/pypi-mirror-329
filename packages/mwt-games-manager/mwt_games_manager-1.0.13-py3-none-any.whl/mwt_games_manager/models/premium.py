from dataclasses import dataclass


@dataclass
class Premium:
    name: str = ""
    trial: bool = False
    trial_end: str = None  # datetime object
