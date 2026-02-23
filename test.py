from sqlalchemy import insert,text,update
from app.utils.database import engine,async_session
import asyncio

from app.utils.schemas import *

from app.closemanager import CloseManager

from app.utils.models import CloseORM,CloseMemberORM,UserORM

async def test():

    source = CloseCreateSchema(type=CloseType.RANDOM,
                    managechannel=0,
                    waitingchannel=0,
                    creator=5,
                    message=0,
                    messagechannel=0,                   
    )

    clm = CloseManager(db=async_session)
    data = await clm.create_close(close_data=source)
    
    print(f'{data=}')
    
    await clm.update_close(data.id,CloseUpdateSchema(lastcall=100))
    close = await clm.getCloseByCreator(5)
    
    print(f"{close=}")
    
    closemember = CloseMemberCreateSchema(
        discord_id=10,
        pos=1,
        team=TeamType.DARK,
        close_id=data.id
    )
    await clm.append_member(data.id,closemember)
    closemember = CloseMemberCreateSchema(
        discord_id=11,
        pos=2,
        team=TeamType.DARK,
        close_id=data.id
    )
    await clm.append_member(data.id,closemember)

    close = await clm.getCloseByCreator(5)
    
    print(f"{close=}")

    members = await clm.get_members(data.id)
    member = await clm.get_member(10)
    
    print(f'{members=}')
    print(f'{member=}')
    
    await clm.create_user(11)
    user = await clm.get_user(11)
    
    print(f"{user=}")
    
    await clm.delete_user(11)
    await clm.delete_close(5)

# asyncio.run(test())

import datetime 

now = datetime.datetime.now()
time = datetime.datetime.fromtimestamp(1754875836)

print((now - time).seconds)

#MTAwMjIyMTYxMTM4NDA2MjAyNA.GAwuW_.CjeBkX8efbuzUSf0Z3ZnNnHS7uoa61KmxnvkC8

    # "Knife": "<:freeiconsword842082:1405556977014407168>",
    # "Onion": "<:freeiconbow1885298:1405557001982967919>",
    # "Security": "<:freeiconshield3077175:1405557022908350654>",
    # "Conhand": "<:freeiconhand1534403:1405557053618913320>",
    # "Conhands": "<:freeiconheart3477186:1405557077807468585>",