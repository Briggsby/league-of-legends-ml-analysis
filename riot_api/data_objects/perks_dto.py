from dataclasses import dataclass
from typing import List

from riot_api.data_objects.dto import Dto
from riot_api.data_objects.perk_stats_dto import PerkStatsDto
from riot_api.data_objects.perk_style_dto import PerkStyleDto


@dataclass
class PerksDto(Dto):
    statPerks: PerkStatsDto
    styles: List[PerkStyleDto]
