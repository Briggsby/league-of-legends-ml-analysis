from dataclasses import dataclass
from typing import List

from riot_api.data_objects.dto import Dto


@dataclass
class MetadataDto(Dto):
    dataVersion: str
    matchId: str
    participants: List[str]
