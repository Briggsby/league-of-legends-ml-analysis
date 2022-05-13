from dataclasses import dataclass
from typing import Optional

from riot_api.data_objects.dto import Dto
from riot_api.data_objects.mini_series_dto import MiniSeriesDto


@dataclass
class LeagueEntryDto(Dto):
    summonerId: str
    summonerName: str
    queueType: str
    leaguePoints: int
    wins: int
    losses: int
    hotStreak: bool
    veteran: bool
    freshBlood: bool
    inactive: bool

    leagueId: Optional[str] = None
    tier: Optional[str] = None
    rank: Optional[str] = None
    miniSeries: Optional[MiniSeriesDto] = None
