from dataclasses import dataclass
from typing import List

from riot_api.data_objects.dto import Dto
from riot_api.data_objects.perk_style_selection_dto import PerkStyleSelectionDto


@dataclass
class PerkStyleDto(Dto):
    description: str
    selections: List[PerkStyleSelectionDto]
    style: int
