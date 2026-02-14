from dataclasses import dataclass
from enum import Enum


class Status(str, Enum):
    RECEIVED = "recibida"
    IN_PROGRESS = "en_proceso"
    OBSERVED = "observada"
    FINISHED = "finalizada"


@dataclass
class Request:
    id: str
    request_type: str
    description: str
    department: str
    priority: str
    status: Status = Status.RECEIVED
