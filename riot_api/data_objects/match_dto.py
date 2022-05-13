from dataclasses import dataclass

from riot_api.data_objects.dto import Dto
from riot_api.data_objects.info_dto import InfoDto
from riot_api.data_objects.metadata_dto import MetadataDto


@dataclass
class MatchDto(Dto):
    metadata: MetadataDto
    info: InfoDto


if __name__ == '__main__':
    test = {'metadata': {'test': 's'}, 'info': {'test': 's'}}
    MatchDto(**test)
