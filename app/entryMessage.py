import random

from collections import defaultdict

import disnake as dis
from disnake import Embed, ui
from disnake.ui import Container

from app.client import CloseBot
from app.utils.models import TeamType
from app.utils.schemas import CloseSchema,CloseMemberSchema


async def update_message(bot: CloseBot, close_id:int) -> Embed:
    members = await bot.clm.get_members(close_id)
    embed = Embed.from_dict(
        {
            "title": "Dota 2 ・ Запись  ᅠ  ᅠ  ᅠ  ᅠ  ᅠ  ᅠ",
            "color": 3092790,
            "fields": [
                {
                    "name": "Силы тьмы",
                            "value": f'{bot.settings.emojis.Knife}・{next((f'<@{x.discord_id}>' for x in members if x.pos == 1 and x.team == TeamType.DARK), "Лёгкая")} \n\n{bot.settings.emojis.Onion}・{next((f'<@{x.discord_id}>' for x in members if x.pos == 2 and x.team == TeamType.DARK), "Центр")} \n\n{bot.settings.emojis.Security}・{next((f'<@{x.discord_id}>' for x in members if x.pos == 3 and x.team == TeamType.DARK), "Сложная")} \n\n{bot.settings.emojis.Conhand}・{next((f'<@{x.discord_id}>' for x in members if x.pos == 4 and x.team == TeamType.DARK), "Частичная поддержка")} \n\n{bot.settings.emojis.Conhands}・{next((f'<@{x.discord_id}>' for x in members if x.pos == 5 and x.team == TeamType.DARK), "Полная поддержка")}',
                    "inline": True
                },
                {
                    "name": "Силы света",
                            "value": f'{bot.settings.emojis.Knife}・{next((f'<@{x.discord_id}>' for x in members if x.pos == 1 and x.team == TeamType.LIGHT), "Лёгкая")} \n\n{bot.settings.emojis.Onion}・{next((f'<@{x.discord_id}>' for x in members if x.pos == 2 and x.team == TeamType.LIGHT), "Центр")} \n\n{bot.settings.emojis.Security}・{next((f'<@{x.discord_id}>' for x in members if x.pos == 3 and x.team == TeamType.LIGHT), "Сложная")} \n\n{bot.settings.emojis.Conhand}・{next((f'<@{x.discord_id}>' for x in members if x.pos == 4 and x.team == TeamType.LIGHT), "Частичная поддержка")}\n\n{bot.settings.emojis.Conhands}・{next((f'<@{x.discord_id}>' for x in members if x.pos == 5 and x.team == TeamType.LIGHT), "Полная поддержка")}',
                    "inline": True
                }
            ]
        }
    )
    return embed

# async def shuffle_message(bot:CloseBot,close_id:int, close:CloseSchema = None) -> list[Container] | Container:
#     container = ui.Container(
#         ui.TextDisplay("# Dota 2 ・ Запись  ᅠ  ᅠ  ᅠ  ᅠ  ᅠ  ᅠ"),
        
#     )

async def update_v2_message(bot:CloseBot,close_id:int, close:CloseSchema = None) -> list[Container,dis.ui.ActionRow]:
    if not(close):
        close = await bot.clm.getCloseById(close_id)
    
    pos_1:list[str] = [
        f"<@{x.discord_id}>" for x in close.members if x.pos == 1
    ]
    pos_2:list[str] = [
        f"<@{x.discord_id}>" for x in close.members if x.pos == 2
    ]
    pos_3:list[str] = [
        f"<@{x.discord_id}>" for x in close.members if x.pos == 3
    ]
    pos_4:list[str] = [
        f"<@{x.discord_id}>" for x in close.members if x.pos == 4
    ]
    pos_5:list[str] = [
        f"<@{x.discord_id}>" for x in close.members if x.pos == 5
    ]
    
    components = ui.Container(
        ui.TextDisplay("# Dota 2 ・ Запись  ᅠ  ᅠ  ᅠ  ᅠ  ᅠ  ᅠ"),
        ui.Section(
            ui.TextDisplay(bot.settings.emojis.Knife + "   " + ",".join(pos_1)),
            accessory=
            dis.ui.Button(
                label="Записатьтся",
                style=dis.ButtonStyle.green,
                custom_id=f"pos.1.random.{close.id}",
                disabled=True if len(pos_1) == 2 else False
            )),
        ui.Section(
            ui.TextDisplay(bot.settings.emojis.Onion + "   " + ",".join(pos_2)),
            accessory=
            dis.ui.Button(
                label="Записатьтся",
                style=dis.ButtonStyle.green,
                custom_id=f"pos.2.random.{close.id}",
                disabled=True if len(pos_2) == 2 else False
            )),
        ui.Section(
            ui.TextDisplay(bot.settings.emojis.Security + "   " + ",".join(pos_3)),
            accessory=
            dis.ui.Button(
                label="Записатьтся",
                style=dis.ButtonStyle.green,
                custom_id=f"pos.3.random.{close.id}",
                disabled=True if len(pos_3) == 2 else False
            )),
        ui.Section(
            ui.TextDisplay(bot.settings.emojis.Conhand + "   " + ",".join(pos_4)),
            accessory=
            dis.ui.Button(
                label="Записатьтся",
                style=dis.ButtonStyle.green,
                custom_id=f"pos.4.random.{close.id}",
                disabled=True if len(pos_4) == 2 else False
            )),
        ui.Section(
            ui.TextDisplay(bot.settings.emojis.Conhands + "   " + ",".join(pos_5)),
            accessory=
            dis.ui.Button(
                label="Записатьтся",
                style=dis.ButtonStyle.green,
                custom_id=f"pos.5.random.{close.id}",
                disabled=True if len(pos_5) == 2 else False
            )),
        accent_colour=dis.Colour.from_hex("#2F3136")
            )
    row = dis.ui.ActionRow.with_message_components()
    row.add_button(
        style=dis.ButtonStyle.danger,
        label="Выйти из записи",
        custom_id=f'closeexit.{close.id}'
    )
    return [components,row]