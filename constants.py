from enum import Enum

BASE_URL = "https://{region}.api.riotgames.com"
BASE_URL_V4 = "https://{region}.api.riotgames.com"

LOL_MATCH_HISTORY_URL = "/lol/match/v5/matches/by-puuid/{puuid}/ids"
LOL_MATCH_URL = "/lol/match/v5/matches/{matchId}"
LOL_LEAGUE_URL = "/lol/league/v4/entries/by-summoner/{encryptedSummonerId}"


class QueueIds(Enum):
    RANKED_SOLO = 420
    RANKED_FLEX = 440
