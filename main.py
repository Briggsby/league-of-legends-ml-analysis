import datetime
import os

import pandas as pd

from constants import QueueIds
from riot_api.api import Api
from scraper import Scraper

token = os.getenv("RIOT_API_TOKEN")
start_puuids = [
    "wHSXXSK8JFN4TdVNrkiN7eS6c3UoVpHdTAj4syqMg042iJqLb7SjPGLMgtXhPg_ggipR9HREI9dzQA",  # Briggsby 12.10
    "34_1PwmUyGJJVzyVNLT8X_kFuo_sg0LUbLBlis-B10tP-Vv8vbaTJDDzxdVIlVU9OmZP2oMuysAK9g",  # SunnyPolarBear 12.10
]

games_csv = 'data/games.csv'
participants_csv = 'data/participants.csv'
players_csv = 'data/players.csv'

start_date = datetime.datetime(2022, 5, 26, 0, 0, 0)
queue_id = QueueIds.RANKED_SOLO.value


def get_start_puuids(number_puuids: int):
    participants = pd.read_csv(participants_csv)
    return list(
        participants
        .groupby('puuid')['puuid']
        .count()
        .sort_values()
        .iloc[:number_puuids]
        .index
    )


api = Api(riot_token=token)
scraper = Scraper(api, get_start_puuids(5) or start_puuids)
while True:
    puuids = list(scraper.puuids_to_do)
    for puuid in puuids:
        if puuid not in scraper.done_puuids:
            scraper.scrape_player_matches(puuid, queue_id, start_date)


