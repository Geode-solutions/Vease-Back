from opengeodeweb_microservice.schemas import Route, load_schema
from dataclasses_json import DataClassJsonMixin
from opengeodeweb_microservice.schemas import print_dataclass
from dataclasses import dataclass


@dataclass
class Healthcheck(DataClassJsonMixin):
    def __post_init__(self) -> None:
        print_dataclass(self)

    pass


@dataclass
class HealthcheckResponse(DataClassJsonMixin):
    def __post_init__(self) -> None:
        print_dataclass(self)

    message: str


healthcheck_route = Route(
    schema=load_schema(__file__),
    params=Healthcheck,
    response=HealthcheckResponse,
)

__all__ = ["Healthcheck", "HealthcheckResponse", "healthcheck_route"]
