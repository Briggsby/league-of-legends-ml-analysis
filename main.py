import datetime
import os

import pandas as pd

from constants import QueueIds
from riot_api.api import Api
from scraper import Scraper

token = os.getenv("RIOT_API_TOKEN")
start_puuid = "uY7OclrYLNVoEr3DfYrta1E4EQrFNp4tSrD-e9xMUecHfSB_LTBsBryvSW8fa5wcZSjd1Qog9RsoKA"

games_csv = 'data/games.csv'
participants_csv = 'data/participants.csv'
players_csv = 'data/players.csv'

start_date = datetime.datetime(2022, 5, 1, 0, 0, 0)
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
scraper = Scraper(api, get_start_puuids(5) or [start_puuid])
while True:
    puuids = list(scraper.puuids_to_do)
    for puuid in puuids:
        if puuid not in scraper.done_puuids:
            scraper.scrape_player_matches(puuid, queue_id, start_date)


