from typing import Optional

from pydantic import BaseModel

from app.utils.models import CloseType, TeamType


class CloseMemberSchema(BaseModel):
    id:int | None = None
    discord_id:int
    pos:int
    team: TeamType
    close_id:int
    class Config:
        from_attributes = True  

class CloseMemberCreateSchema(BaseModel):
    discord_id:int
    pos:int
    team: TeamType
    close_id:int
    class Config:
        from_attributes = True 

class CloseSchema(BaseModel):
    id: int | None = None
    type:CloseType
    managechannel:int
    waitingchannel:int
    creator:int
    lastcall:int | None = None
    message:int | None = None
    messagechannel:int
    members:list[CloseMemberSchema] | list
    class Config:
        from_attributes = True  

class CloseCreateSchema(BaseModel):
    type: CloseType
    managechannel: int
    waitingchannel: int
    creator: int
    messagechannel: int
    message: int | None = None

class CloseUpdateSchema(BaseModel):
    lastcall: Optional[int] = None
    message: Optional[int] = None

class UserSchema(BaseModel):
    userid:int
    pos1games: int = 0
    pos1wins: int = 0 
    pos2games: int = 0
    pos2wins: int = 0
    pos3games: int = 0
    pos3wins: int = 0
    pos4games: int = 0
    pos4wins: int = 0
    pos5games: int = 0
    pos5wins: int = 0
    class Config:
        from_attributes = True
