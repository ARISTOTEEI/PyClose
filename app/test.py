from sqlalchemy import insert,text
from database import engine,async_session
from schemas import Close
import asyncio

async def inser_data():
    close_1 = Close(type = "random",managechannel = 0,waitingchannel = 0,creator = 0,lastcall = 0,message = 0,messagechannel = 0)
    async with async_session() as s:
        s.add(close_1)
        await s.commit()

asyncio.run(inser_data())