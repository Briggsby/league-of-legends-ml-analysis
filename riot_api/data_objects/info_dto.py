from dataclasses import dataclass
from typing import List, Optional

from riot_api.data_objects.dto import Dto
from riot_api.data_objects.participant_dto import ParticipantDto
from riot_api.data_objects.team_dto import TeamDto


@dataclass
class InfoDto(Dto):
    gameCreation: int
    gameDuration: int
    gameId: int
    gameMode: str
    gameName: str
    gameStartTimestamp: int
    gameType: str
    gameVersion: str
    mapId: int
    participants: List[ParticipantDto]
    platformId: str
    queueId: int
    teams: List[TeamDto]

    gameEndTimestamp: Optional[int] = None
    tournamentCode: Optional[str] = None
