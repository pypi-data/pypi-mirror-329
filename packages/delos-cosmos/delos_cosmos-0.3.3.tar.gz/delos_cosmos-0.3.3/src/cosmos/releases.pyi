from datetime import datetime
from enum import Enum
from typing import Any

from _typeshed import Incomplete
from pydantic import BaseModel

from .endpoints import CosmosEndpoints as CosmosEndpoints
from .endpoints import Endpoints as Endpoints

class Release(Enum):
    V1 = "v1"

class CosmosClientReleases(BaseModel):
    version: Release
    release_date: datetime
    details: dict[str, Any]
    suffix: str
    available_endpoints: list[CosmosEndpoints]

first_release: Incomplete
AllReleases: list[CosmosClientReleases]
