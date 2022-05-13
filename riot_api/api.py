import datetime
import http
import time
from typing import Type, List, Optional, Union

import requests

from constants import LOL_MATCH_HISTORY_URL, LOL_MATCH_URL, LOL_LEAGUE_URL, \
    BASE_URL, BASE_URL_V4
from riot_api.data_objects.league_entry_dto import LeagueEntryDto
from riot_api.data_objects.match_dto import MatchDto


class Api:
    SECONDS_BETWEEN_REQUESTS = 120 / 100  # 100 per 2 minutes
    TOKEN_HEADER = 'X-Riot-Token'

    def __init__(self, riot_token: str, region: str = "euw1"):
        self.riot_token = riot_token
        self.region = region
        self.base_url = BASE_URL.format(
            region=region if region != "euw1" else "europe"
        )
        self.base_url_v4 = BASE_URL_V4.format(region=region)
        self.next_request = datetime.datetime.now()

    def get_headers(self):
        return {self.TOKEN_HEADER: self.riot_token}

    def make_request(
        self,
        url: str,
        params: Optional[dict] = None,
        body: Optional[dict] = None,
    ):
        if datetime.datetime.now() < self.next_request:
            time.sleep((self.next_request - datetime.datetime.now()).seconds)

        response = requests.get(
            url, params, json=body, headers=self.get_headers()
        )
        self.next_request = (
                datetime.datetime.now()
                + datetime.timedelta(seconds=self.SECONDS_BETWEEN_REQUESTS)
        )
        if response.status_code != http.HTTPStatus.OK:
            raise Exception(
                f"Error making request. "
                f"Status Code: {str(response.status_code)} "
                f"Response: {str(response.json())}"
            )

        return response.json()

    def get_lol_match_history(
        self,
        puuid: str,
        queue: int,
        start: datetime.datetime = None,
        end: datetime.datetime = None,
    ) -> List[str]:
        url = self.base_url + LOL_MATCH_HISTORY_URL.format(puuid=puuid)
        return self.make_request(
            url,
            params={
                "queue": queue,
                **({"startTime": int(start.timestamp())} if start else {}),
                **({"endTime": int(end.timestamp())} if end else {}),
            }
        )

    def get_lol_match(self, match_id: str) -> MatchDto:
        url = self.base_url + LOL_MATCH_URL.format(matchId=match_id)
        response = self.make_request(url)
        return MatchDto(**response)

    def get_lol_league_by_summoner_id(
        self,
        summoner_id
    ) -> List[LeagueEntryDto]:
        url = self.base_url_v4 + LOL_LEAGUE_URL.format(
            encryptedSummonerId=summoner_id,
        )
        response = self.make_request(url)
        return [LeagueEntryDto(**res) for res in response]

