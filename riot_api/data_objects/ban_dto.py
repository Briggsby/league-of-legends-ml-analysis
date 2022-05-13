from dataclasses import dataclass

from riot_api.data_objects.dto import Dto


@dataclass
class BanDto(Dto):
    championId: int
    pickTurn: int
