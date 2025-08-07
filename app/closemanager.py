from sqlalchemy.ext.asyncio import AsyncSession,async_sessionmaker
from sqlalchemy import update,select,insert,delete
from app.utils.schemas import *
from app.utils.models import CloseORM,CloseMemberORM,UserORM
from pydantic import ValidationError

class CloseManager:
    def __init__(self,db:async_sessionmaker[AsyncSession]):
        self.db = db
    
    #CloseMethods

    async def create_close(self,close_data:CloseCreateSchema) -> CloseSchema:
        async with self.db() as session:
            stmt = (
                insert(CloseORM)
                .values(**close_data.model_dump())

            )
            await session.execute(stmt)
            await session.commit()
            return await self.getCloseByCreator(close_data.creator)

    async def getCloseByCreator(self,creator_id:int) -> CloseSchema:
        async with self.db() as session:
            stmt = (
                select(CloseORM)
                .filter_by(creator = creator_id)
            )
            close = await session.execute(stmt)
            try:
                close = CloseSchema.model_validate(close.scalar_one_or_none())
            except Exception:
                close = None
            return close

    async def getCloseById(self,close_id:int) -> CloseSchema:
        async with self.db() as session:
            close = await session.get(CloseORM,close_id)
            return CloseSchema.model_validate(close)

    async def update_close(self,id:int,close_data:CloseUpdateSchema) -> None:
        async with self.db() as session:
            stmt = (
                update(CloseORM)
                .values(**close_data.model_dump())
                .filter_by(id = id)
            )
            await session.execute(stmt)
            await session.commit()
    
    async def delete_close(self,creator_id:int) -> None:
        async with self.db() as session:
            stmt = (
                delete(CloseORM)
                .filter_by(creator = creator_id)
            )
            await session.execute(stmt)
            await session.commit()
    
    #Close Member Methods

    async def append_member(self,close_id:int,member:CloseMemberCreateSchema) -> None:
        async with self.db() as session:
            member = CloseMemberORM(**member.model_dump())
            session.add(member)
            await session.commit()

    async def get_members(self,close_id:int) -> List[CloseMemberSchema]:
        async with self.db() as session:
            stmt = (
                select(CloseMemberORM)
                .filter_by(close_id = close_id)
            )
            members = await session.execute(stmt)
            members = [CloseMemberSchema.model_validate(i) for i in members.scalars().all()]
            return members

    async def delete_member(self,discord_id:int):
        async with self.db() as session:
            stmt = (
                delete(CloseMemberORM)
                .filter_by(discord_id = discord_id)
            )
            await session.execute(stmt)
            await session.commit()


    async def get_member(self,discord_id:int) -> CloseMemberSchema:
        async with self.db() as session:
            stmt = (
                select(CloseMemberORM)
                .filter_by(discord_id = discord_id)
            )
            data = await session.execute(stmt)
            data = data.scalar_one_or_none()
            if data != None:
                data = CloseMemberSchema.model_validate(data,from_attributes=True)
                return data
            else:
                return None

    async def edit_member(self,discord_id:int,pos:int,team:TeamType) -> None:
        async with self.db() as session:
            stmt = (
                update(CloseMemberORM)
                .values(pos = pos,team = team)
                .filter_by(discord_id = discord_id)
            )
            await session.execute(stmt)
            await session.commit()

 
    #User methods

    async def create_user(self,user_id:int) -> None:
        async with self.db() as session:
            user = UserORM(userid = user_id)
            session.add(user)
            await session.commit()

    async def get_user(self,user_id:int) -> UserSchema:
        async with self.db() as session:
            stmt = (
                select(UserORM)
                .filter_by(userid = user_id)
            )
            data = await session.execute(stmt)
            data = data.scalar_one_or_none()
            data = UserSchema.model_validate(data)
            return data

    async def update_user(self,user:UserSchema) -> None:
        async with self.db() as session:
            stmt = (
                update(UserORM)
                .values(**user.model_dump())
                .filter_by(userid = user.userid)
            )
            await session.execute(stmt)
            await session.commit()

    async def delete_user(self,user_id:int) -> None:
        async with self.db() as session:
            stmt = (
                delete(UserORM)
                .filter_by(userid = user_id)
            )
            await session.execute(stmt)
            await session.commit()

    # async def create_clmember(self,user_id):
    #     async with self.db() as session:
    #         member = CloseMemberORM(userid = user_id)
    #         await session.add(member)   
    #         await session.commit()

    # async def getClmemberByUSID(self,user_id:int) -> CloseMembersSource:
    #     async with self.db() as session:
    #         stmt = (
    #             select(CloseMemberORM)
    #             .filter_by(userid = user_id)
    #         )
    #         member = await session.execute(stmt)
    #         member = member.scalar_one_or_none()
    #         member = CloseMembersSource.model_validate(member,from_attributes=True)
    #         await session.commit()
    #         return member

    # async def update_clmember(self,member_data:CloseMembersSource):
    #     async with self.db() as session:
    #         stmt = (
    #             update(CloseMemberORM)
    #             .values(**member_data.model_dump())
    #             .filter_by(userid = member_data.userid)
    #         )
    #         await session.execute(stmt)
    #         await session.commit()