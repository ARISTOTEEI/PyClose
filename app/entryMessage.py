from sqlalchemy.ext.asyncio import AsyncSession,async_sessionmaker
from disnake import Message,Embed
from app.client import CloseBot
async def update_message(bot:CloseBot,db:async_sessionmaker[AsyncSession]) -> Message:
    embed = Embed.from_dict(
            message = Embed.from_dict(
                {
                        "title": "Dota 2 ・ Запись  ᅠ  ᅠ  ᅠ  ᅠ  ᅠ  ᅠ",
                        "color": 3092790,
                        "fields": [
                        {
                            "name": "Силы тьмы",
                            "value": f'{bot.settings.emojis.Knife}・Лёгкая \n\n{bot.settings.emojis.Onion}・Центр \n\n{bot.settings.emojis.Security}・Сложная \n\n{bot.settings.emojis.Conhand}・Частичная поддержка\n\n{bot.settings.emojis.Conhands}・Полная поддержка',
                            "inline": True
                        },
                        {
                            "name": "Силы света",
                            "value": f'{bot.settings.emojis.Knife}・Лёгкая \n\n{bot.settings.emojis.Onion}・Центр \n\n{bot.settings.emojis.Security}・Сложная \n\n{bot.settings.emojis.Conhand}・Частичная поддержка\n\n{bot.settings.emojis.Conhands}・Полная поддержка',
                            "inline": True
                        }
                        ]
                }
            )
    )