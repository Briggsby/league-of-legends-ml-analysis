from dataclasses import dataclass

from riot_api.data_objects.dto import Dto


@dataclass
class PerkStyleSelectionDto(Dto):
    perk: int
    var1: int
    var2: int
    var3: int
