from sqlalchemy.ext.asyncio import AsyncSession,async_sessionmaker
from sqlalchemy import update,select
from enum import Enum
from app.utils.schemas import Closes as CloseORM
from app.utils.schemas import CloseMembers as CloseMemberORM
from pydantic import BaseModel

class CloseType(str,Enum):
    COMMAND = 'command'
    RANDOM = 'random'


class CloseSource(BaseModel):
    id: int | None = None
    type:CloseType
    managechannel:int
    waitingchannel:int
    creator:int
    lastcall:int | None = None
    message:int
    messagechannel:int

class CloseMembersSource(BaseModel):
    userid:int
    closeid:int | None = None
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

class CloseManager:
    def __init__(self,db:async_sessionmaker[AsyncSession]):
        self.db = db
    
    async def create_close(self,close_data:CloseSource) -> None:
        async with self.db() as session:
            close = CloseORM(**close_data.model_dump())
            session.add(close)
            await session.commit()

    async def update_close(self,id:int,close_data:CloseSource) -> None:
        async with self.db() as session:
            stmt = (
                update(CloseORM)
                .values(**close_data.model_dump())
                .filter_by(id = id)
            )
            await session.execute(stmt)
            await session.commit()
    
    async def getCloseByID(self,id:int) -> CloseSource:
        async with self.db() as session:
            close = await session.get(CloseORM,id)
            close = CloseSource.model_validate(close,from_attributes=True)
            await session.commit()
            return close

    async def getCloseByCreator(self,creator_id:int) -> CloseSource:
        async with self.db() as session:
            stmt = (
                select(CloseORM)
                .filter_by(creator = creator_id)
            )
            close = await session.execute(stmt)
            try:
                close = CloseSource.model_validate(close.scalar_one_or_none(),from_attributes=True)
            except:
                close = None
            return close
    
    async def create_clmember(self,user_id):
        async with self.db() as session:
            member = CloseMemberORM(userid = user_id)
            await session.add(member)   
            await session.commit()

    async def getClmemberByUSID(self,user_id:int) -> CloseMembersSource:
        async with self.db() as session:
            stmt = (
                select(CloseMemberORM)
                .filter_by(userid = user_id)
            )
            member = await session.execute(stmt)
            member = member.scalar_one_or_none()
            member = CloseMembersSource.model_validate(member,from_attributes=True)
            await session.commit()
            return member

    async def update_clmember(self,member_data:CloseMembersSource):
        async with self.db() as session:
            stmt = (
                update(CloseMemberORM)
                .values(**member_data.model_dump())
                .filter_by(userid = member_data.userid)
            )
            await session.execute(stmt)
            await session.commit()