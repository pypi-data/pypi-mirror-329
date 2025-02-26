import hashlib
from datetime import datetime
from enum import Enum

from pydantic import BaseModel
from pydantic.dataclasses import dataclass


@dataclass(frozen=True)
class ExporterInstance:
    ip_addr: str
    port: int
    hostname: str

    @property
    def id(self):
        unique_string = f"{self.ip_addr}:{self.port}:{self.hostname}"
        return hashlib.md5(unique_string.encode()).hexdigest()


class HealthResponse(BaseModel):
    status: str
    timestamp: datetime
    version: str


class RegistrationResponse(BaseModel):
    status: str
    message: str


class RegistrationStatus(Enum):
    UNREGISTERED = "unregistered"
    REGISTERED = "registered"
    ATTEMPTING = "attempting"
    FAILED = "failed"


class MetricType(str, Enum):
    CPU = "cpu"
    MEMORY = "memory"
    STORAGE = "storage"
    NETWORK = "network"
