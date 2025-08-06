from sqlalchemy.ext.asyncio import AsyncSession,async_sessionmaker
from disnake import Message,Embed
from app.client import CloseBot
from app.utils.models import TeamType

async def update_message(bot:CloseBot,close_id) -> Embed:
    members = await bot.clm.get_members(close_id)
    embed = Embed.from_dict(
                {
                        "title": "Dota 2 ・ Запись  ᅠ  ᅠ  ᅠ  ᅠ  ᅠ  ᅠ",
                        "color": 3092790,
                        "fields": [
                        {
                            "name": "Силы тьмы",
                            "value": f'{bot.settings.emojis.Knife}・{next((x for x in members if x.pos == 1 and x.team == TeamType.DARK),"Лёгкая")} \n\n{bot.settings.emojis.Onion}・{next((x for x in members if x.pos == 2 and x.team == TeamType.DARK),"Центр")} \n\n{bot.settings.emojis.Security}・{next((x for x in members if x.pos == 3 and x.team == TeamType.DARK),"Сложная")} \n\n{bot.settings.emojis.Conhand}・{next((x for x in members if x.pos == 4 and x.team == TeamType.DARK),"Частичная поддержка")} \n\n{bot.settings.emojis.Conhands}・{next((x for x in members if x.pos == 5 and x.team == TeamType.DARK),"Полная поддержка")}',
                            "inline": True
                        },
                        {
                            "name": "Силы света",
                            "value": f'{bot.settings.emojis.Knife}・{next((x for x in members if x.pos == 1 and x.team == TeamType.LIGHT),"Лёгкая")} \n\n{bot.settings.emojis.Onion}・{next((x for x in members if x.pos == 2 and x.team == TeamType.LIGHT),"Центр")} \n\n{bot.settings.emojis.Security}・{next((x for x in members if x.pos == 3 and x.team == TeamType.LIGHT),"Сложная")} \n\n{bot.settings.emojis.Conhand}・{next((x for x in members if x.pos == 4 and x.team == TeamType.LIGHT),"Частичная поддержка")}\n\n{bot.settings.emojis.Conhands}・{next((x for x in members if x.pos == 5 and x.team == TeamType.LIGHT),"Полная поддержка")}',
                            "inline": True
                        }
                        ]
                }
    )
    return embed
