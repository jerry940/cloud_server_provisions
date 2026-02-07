from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field, IPvAnyAddress, ConfigDict

class ServerState(str, Enum):
    active = "active"
    offline = "offline"
    retired = "retired"

class ServerCreate(BaseModel):
    hostname: str = Field(min_length=1, max_length=255)
    ip_address: IPvAnyAddress
    state: ServerState

class ServerUpdate(BaseModel):
    hostname: Optional[str] = Field(default=None, min_length=1, max_length=255)
    ip_address: Optional[IPvAnyAddress] = None
    state: Optional[ServerState] = None

class ServerOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    hostname: str
    ip_address: str 
    state: ServerState
