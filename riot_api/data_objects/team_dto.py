from dataclasses import dataclass
from typing import List

from riot_api.data_objects.ban_dto import BanDto
from riot_api.data_objects.dto import Dto
from riot_api.data_objects.objectives_dto import ObjectivesDto


@dataclass
class TeamDto(Dto):
    bans: List[BanDto]
    objectives: ObjectivesDto
    teamId: int
    win: bool
