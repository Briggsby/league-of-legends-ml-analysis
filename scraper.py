import datetime
from typing import Iterable

import pandas as pd

from data_models import Game, Player, GameParticipant
from riot_api.api import Api


class Scraper:
    GAMES_OUTPUT = "/games.csv"
    PARTICIPANTS_OUTPUT = "/participants.csv"
    PLAYERS_OUTPUT = "/players.csv"

    def __init__(
            self,
            api: Api,
            start_puuids: Iterable[str],
            data_folder_path: str = "./data",
    ):
        self.api = api
        self.games_file = data_folder_path + self.GAMES_OUTPUT
        self.participants_file = data_folder_path + self.PARTICIPANTS_OUTPUT
        self.players_file = data_folder_path + self.PLAYERS_OUTPUT

        self.done_match_ids = self.get_done_match_ids()
        self.done_participants = self.get_done_participants()
        self.done_players = self.get_done_players()

        self.puuids_to_do = set(start_puuids)
        self.done_puuids = set()

    def get_done_match_ids(self):
        matches = pd.read_csv(self.games_file)
        return set(matches["id"])

    def get_done_participants(self):
        participants = pd.read_csv(self.participants_file)
        participants = participants[["game_id", "index"]]
        return set(participants.itertuples(index=False))

    def get_done_players(self):
        players = pd.read_csv(self.players_file)
        players = players[["summoner_id", "snapshot_at"]]
        players["snapshot_at"] = pd.to_datetime(players["snapshot_at"])
        players["snapshot_at"] = (
                players["snapshot_at"]
                - pd.to_timedelta(players["snapshot_at"].dt.dayofweek, unit='d')
        ).dt.date
        return set(players.itertuples(index=False))

    def scrape_player_matches(
            self,
            puuid: str,
            queue_id: int,
            start: datetime.datetime = None,
            end: datetime.datetime = None,
    ):
        match_ids = self.api.get_lol_match_history(puuid, queue_id, start, end)
        for match_id in match_ids:
            if match_id in self.done_match_ids:
                continue

            match_dto = self.api.get_lol_match(match_id)
            game = Game.from_match(match_dto)
            for index, participant in enumerate(match_dto.info.participants):
                summoner_id = participant.summonerId

                if (match_id, summoner_id) in self.done_participants:
                    continue

                now = datetime.datetime.now()
                start_of_week = (
                    now - datetime.timedelta(days=now.weekday())
                ).date()
                if (summoner_id, start_of_week) in self.done_players:
                    continue

                league_dtos = self.api.get_lol_league_by_summoner_id(
                    summoner_id
                )
                for league_dto in league_dtos:
                    player = Player.from_league(
                        participant.puuid,
                        league_dto,
                        now
                    )
                    player.write_to_csv(self.players_file)
                    self.done_players.add((summoner_id, start_of_week))

                game_participant = GameParticipant.from_participant(
                    match_dto, index, participant
                )
                game_participant.write_to_csv(self.participants_file)
                self.done_participants.add((match_id, index))

                if (
                        game_participant.puuid not in self.done_puuids
                        and game_participant.puuid != puuid
                ):
                    self.puuids_to_do.add(game_participant.puuid)

            game.write_to_csv(self.games_file)
            self.done_match_ids.add(match_id)

        self.puuids_to_do.remove(puuid)
        self.done_puuids.add(puuid)
