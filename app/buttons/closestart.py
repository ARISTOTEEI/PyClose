import random
from collections import defaultdict

import disnake as dis
from disnake import PermissionOverwrite
from disnake.ext import commands
from disnake.ext.commands import Cog

from app.client import CloseBot
from app.entrymessage import update_message
from app.utils.schemas import CloseMemberSchema


async def split_teams(players:list[CloseMemberSchema] ) -> tuple[list[CloseMemberSchema], list[CloseMemberSchema]]:
    by_position = defaultdict(list)
    for player in players:
        by_position[player.pos].append(player)

    team1, team2 = [], []
    for pos, group in by_position.items():  # noqa: PERF102
        random.shuffle(group)

        if len(group) >= 2:
            team1.append(group[0])
            team2.append(group[1])

        if len(group) % 2 != 0:
            extra_player = group[0]
            if len(team1) <= len(team2):
                team1.append(extra_player)
            else:
                team2.append(extra_player)

    return team1, team2


class CloseStartButton(Cog):
    def __init__(self, bot: CloseBot):
        self.bot = bot
        super().__init__()

    @commands.Cog.listener()
    async def on_button_click(self, inter: dis.MessageInteraction):
        if inter.component.custom_id.startswith("closestart"):
            await inter.response.defer(with_message=True, ephemeral=True)
            raw_data = inter.component.custom_id.split(".")
            close_id = int(raw_data[-1])
            close = await self.bot.clm.getCloseById(close_id)
            members = await self.bot.clm.get_members(close_id)
            if inter.guild.get_role(self.bot.settings.roles.closemod) in inter.author.roles:
                
                if close.creator == inter.author.id:
                    
                    if (2 <= len(members) <= 10) or close.creator == 745562614930604073:
                        
                        await inter.edit_original_message("## Клоз запущен")
                        
                        closeban = inter.guild.get_role(self.bot.settings.roles.closeban)
                        everyone = inter.guild.default_role
                        category = inter.guild.get_channel(close.managechannel).category
                        closemod = inter.guild.get_role(self.bot.settings.roles.closemod)

                        if channel:=inter.guild.get_channel(close.waitingchannel):
                            await channel.delete()

                        for component in inter.message.components:
                            for child in component.children:
                                if isinstance(child,dis.components.ActionRow):
                                    for button in child.children:
                                        if not(button.custom_id.startswith("closecancel")):
                                            button.disabled = True
                        
                        contain = dis.ui.Container.from_component(inter.message.components[0])
                        await inter.message.edit(components=contain)

                        components = inter.message.components
                        components = dis.ui.ActionRow.with_message_components()
                        components.add_string_select(
                            custom_id=f"closewinner.{close_id}",
                            placeholder="Выбрать победителя",
                            max_values=1,
                            options=[
                                dis.SelectOption(
                                    label="Силы света",
                                    value="light",
                                    description="Силы света",
                                    emoji=self.bot.settings.emojis.light
                                ),
                                dis.SelectOption(
                                    label="Силы тьмы",
                                    value="dark",
                                    description="Силы тьмы",
                                    emoji=self.bot.settings.emojis.dark
                                )
                            ]
                        )
                        message = await inter.guild.get_channel(close.messagechannel).fetch_message(close.message)
                        team_1, team_2 = await split_teams(close.members)
                        if team_1:
                            for member in team_1:
                                await self.bot.clm.edit_member(member.discord_id,member.pos,'dark')
                        if team_2:
                            for member in team_2:
                                await self.bot.clm.edit_member(member.discord_id,member.pos,'light')
                        cont = await update_message(self.bot,close_id)
                        await message.delete()
                        await message.channel.send(embed=cont,components=components)

                        #----------------------------------
                        overwrites = {
                            everyone: PermissionOverwrite(send_messages=False, view_channel=False),
                            closeban: PermissionOverwrite(view_channel=False),
                            closemod: PermissionOverwrite(
                                view_channel=True, send_messages=True, manage_messages=True)
                        }
                        for member in members:
                            user = inter.guild.get_member(member.discord_id)
                            overwrites[user] = PermissionOverwrite(
                                view_channel=True, send_messages=True)

                        lobby = await inter.guild.create_text_channel(
                            name="🎮・Лобби",
                            category=category,
                            overwrites=overwrites,
                            position=2
                        )
                        #----------------------------------
                        
                        #----------------------------------
                        overwrites = {
                            everyone: PermissionOverwrite(view_channel=True, connect=True),
                            closemod: PermissionOverwrite(view_channel=True, kick_members=True),
                            closeban: PermissionOverwrite(view_channel=False)
                        }
                        await inter.guild.create_voice_channel(
                            name='[🎥]просмотр',
                            category=category,
                            overwrites=overwrites
                        )
                        #----------------------------------
                        
                        #----------------------------------
                        overwrites = {
                            everyone: PermissionOverwrite(view_channel=True, connect=False),
                            closemod: PermissionOverwrite(view_channel=True, kick_members=True),
                            closeban: PermissionOverwrite(view_channel=False)
                        }
                        for member in members:
                            if member.team == "dark":
                                user = inter.guild.get_member(
                                    member.discord_id)
                                overwrites[user] = PermissionOverwrite(
                                    connect=False
                                )
                        await inter.guild.create_voice_channel(
                            name='🌕・Силы света',
                            category=category,
                            overwrites=overwrites
                        )
                        #----------------------------------
                        
                        #----------------------------------
                        overwrites = {
                            everyone: PermissionOverwrite(view_channel=True, connect=False),
                            closemod: PermissionOverwrite(view_channel=True, kick_members=True),
                            closeban: PermissionOverwrite(view_channel=False)
                        }
                        for member in members:
                            if member.team == "light":
                                user = inter.guild.get_member(
                                    member.discord_id)
                                overwrites[user] = PermissionOverwrite(
                                    connect=False
                                )
                        await inter.guild.create_voice_channel(
                            name='🌑・Силы тьмы',
                            category=category,
                            overwrites=overwrites
                        )
                        #----------------------------------
                        
                        password = [str(random.randint(1,10)) for i in range(10)]
                        name = f"DOTA2RU{random.randint(1, 4)}"
                        embed = dis.Embed.from_dict(
                            {
                                "title": "Dota 2 ・ Информация ᅠ  ᅠ  ᅠ  ᅠ  ᅠ  ᅠ",
                                "description": "**Готовность:** не создано \n**Название лобби:** " + f"{name}" + "\n**Пароль:** " + f"{''.join(password)}" + "\n**Регион:** Стокгольм",
                                "color": 3092790
                            }
                        )
                        row = dis.ui.ActionRow.with_message_components()
                        row.add_button(
                            style=dis.ButtonStyle.success,
                            label="Сообщить о готовности лобби",
                            custom_id=f"lobbycreated.{close_id}"
                        )
                        await lobby.send(embed=embed, components=row)
                    else:
                        await inter.edit_original_response("## Слишком мало участников")
                else:
                    await inter.edit_original_response("## Вы не являетесь создателем клоза")
            else:
                await inter.edit_original_response("## Вы не являетесь клозмодом")
                


def setup(bot: CloseBot):
    bot.add_cog(CloseStartButton(bot))
