from dataclasses import dataclass


@dataclass
class InfoSchema:
    pearl_id: str


@dataclass
class PearlSchema:
    host: str
    port: int
