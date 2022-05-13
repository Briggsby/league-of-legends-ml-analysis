from dataclasses import dataclass

from riot_api.data_objects.dto import Dto


@dataclass
class MiniSeriesDto(Dto):
    losses: int
    progress: str
    target: int
    wins: int
