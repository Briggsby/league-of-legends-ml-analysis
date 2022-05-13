import datetime
from dataclasses import dataclass, fields, asdict
from typing import List

import pandas as pd

from riot_api.data_objects.league_entry_dto import LeagueEntryDto
from riot_api.data_objects.match_dto import MatchDto
from riot_api.data_objects.participant_dto import ParticipantDto


@dataclass
class DataModel:
    def __post_init__(self):
        for field in fields(self):
            if field.type is datetime.datetime:
                current_value = self.__getattribute__(field.name)

                if isinstance(current_value, int):
                    self.__setattr__(
                        field.name,
                        datetime.datetime.utcfromtimestamp(current_value),
                    )

    # def to_dict(self):
    #     values = asdict(self)
    #     for key, value in values.copy().items():
    #         if isinstance(value, datetime.datetime):
    #             values[key] = value.timestamp()

    def write_to_csv(self, file_path, header=False, mode='a'):
        df = pd.DataFrame([asdict(self)])
        return df.to_csv(file_path, mode=mode, index=False, header=header)


@dataclass
class GameParticipant(DataModel):
    game_id: str
    summoner_id: str
    champ_name: str
    blue_side: bool
    win: bool

    index: int
    puuid: str
    kills: int
    deaths: int
    lane: str
    role: str
    gold_spent: int
    total_damage_dealt_to_champions: int
    damage_dealt_to_objectives: int
    total_damage_taken: int
    wards_placed: int
    wards_killed: int
    vision_score: int
    turret_plates_taken: int
    items: List[int]

    inhibitor_kills: int
    turrets_killed: int
    baron_kills: int
    dragon_kills: int

    inhibitors_lost: int
    turrets_lost: int

    @classmethod
    def from_participant(
            cls, match: MatchDto, index: int, participant: ParticipantDto
    ):
        return cls(
            game_id=match.metadata.matchId,
            summoner_id=participant.summonerId,
            champ_name=participant.championName,
            blue_side=participant.teamId == 100,
            win=participant.win,

            index=index,
            puuid=participant.puuid,
            kills=participant.kills,
            deaths=participant.deaths,
            lane=participant.lane,
            role=participant.role,
            gold_spent=participant.goldSpent,
            total_damage_dealt_to_champions=participant.totalDamageDealtToChampions,
            damage_dealt_to_objectives=participant.damageDealtToObjectives,
            total_damage_taken=participant.totalDamageTaken,
            vision_score=participant.visionScore,
            wards_killed=participant.wardsKilled,
            wards_placed=participant.wardsPlaced,
            turret_plates_taken=participant.challenges.get(
                "turretPlatesTaken", None
            ),
            items=[
                participant.item0, participant.item1, participant.item2,
                participant.item3, participant.item4, participant.item5,
            ],
            inhibitor_kills=participant.inhibitorKills,
            turrets_killed=participant.turretKills,
            baron_kills=participant.baronKills,
            dragon_kills=participant.dragonKills,
            inhibitors_lost=participant.inhibitorsLost,
            turrets_lost=participant.turretsLost,
        )


@dataclass
class Game(DataModel):
    id: str
    queue_id: int
    game_creation: int
    game_duration: int
    game_mode: str
    game_type: str
    game_version: str
    map_id: int

    @classmethod
    def from_match(cls, match: MatchDto):
        return cls(
            id=match.metadata.matchId,
            game_creation=match.info.gameCreation,
            game_duration=match.info.gameDuration,
            queue_id=match.info.queueId,
            game_mode=match.info.gameMode,
            game_type=match.info.gameType,
            game_version=match.info.gameVersion,
            map_id=match.info.mapId,
        )


@dataclass
class Player(DataModel):
    summoner_id: str
    puuid: str
    summoner_name: str
    snapshot_at: int
    rank: str
    tier: str
    wins: int
    losses: int
    hot_streak: bool
    queue_type: str

    @classmethod
    def from_league(
            cls,
            puuid: str,
            league: LeagueEntryDto,
            request_time: datetime.datetime
    ):
        return cls(
            summoner_id=league.summonerId,
            puuid=puuid,
            summoner_name=league.summonerName,
            snapshot_at=int(request_time.timestamp()),
            rank=league.rank,
            tier=league.tier,
            wins=league.wins,
            losses=league.losses,
            hot_streak=league.hotStreak,
            queue_type=league.queueType,
        )
