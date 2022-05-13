from dataclasses import dataclass

from riot_api.data_objects.dto import Dto


@dataclass
class ObjectivesDto(Dto):
    baron: "ObjectiveDto"
    champion: "ObjectiveDto"
    dragon: "ObjectiveDto"
    inhibitor: "ObjectiveDto"
    riftHerald: "ObjectiveDto"
    tower: "ObjectiveDto"


@dataclass
class ObjectiveDto(Dto):
    first: bool
    kills: int
