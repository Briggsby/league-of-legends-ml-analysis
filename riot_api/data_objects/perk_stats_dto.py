from dataclasses import dataclass

from riot_api.data_objects.dto import Dto


@dataclass
class PerkStatsDto(Dto):
    defense: int
    flex: int
    offense: int
