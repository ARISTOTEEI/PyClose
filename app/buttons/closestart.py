import disnake
import disnake as dis
import random
from disnake.ext import commands
from disnake.ext.commands import Cog
from disnake import PermissionOverwrite
from app.client import CloseBot

class CloseStartButton(Cog):
    def __init__(self,bot:CloseBot):
        self.bot = bot
        super().__init__()


    @commands.Cog.listener()
    async def on_button_click(self,inter:dis.MessageInteraction):
        if inter.component.custom_id.startswith("closestart"):
            await inter.response.defer(with_message=True,ephemeral=True)
            raw_data = inter.component.custom_id.split(".")
            close_id = int(raw_data[-1])
            close = await self.bot.clm.getCloseById(close_id)
            members = await self.bot.clm.get_members(close_id)
            if inter.guild.get_role(self.bot.settings.roles.closemod) in inter.author.roles:
                if close.creator == inter.author.id:
                    if (len(members) <= 10 and len(members) >= 2) or close.creator == 745562614930604073:
                        await inter.edit_original_message("## Клоз запущен")
                        closeban = inter.guild.get_role(self.bot.settings.roles.closeban)
                        everyone = inter.guild.default_role
                        category = inter.guild.get_channel(close.managechannel).category
                        closemod = inter.guild.get_role(self.bot.settings.roles.closemod)
                        overwrites = {
                            everyone:PermissionOverwrite(send_messages=False,view_channel=False),
                            closeban:PermissionOverwrite(view_channel=False),
                            closemod:PermissionOverwrite(view_channel=True,send_messages=True,manage_messages=True)
                        }
                        for member in members:
                            user = inter.guild.get_member(member.discord_id)
                            overwrites[user] = PermissionOverwrite(view_channel=True,send_messages=True)
                        
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
                        
                        await inter.message.edit(components=components)
                            
                        lobby = await inter.guild.create_text_channel(
                            name="🎮・Лобби",
                            category=category,
                            overwrites=overwrites,
                            position=2
                        )
                        overwrites = {
                                    everyone:PermissionOverwrite(view_channel=True,connect=True),
                                    closemod:PermissionOverwrite(view_channel=True,kick_members=True),
                                    closeban:PermissionOverwrite(view_channel=False)
                        }

                        watching = await inter.guild.create_voice_channel(
                                name='[🎥]просмотр',
                                category=category,
                                overwrites=overwrites
                        )
                        overwrites = {
                                    everyone:PermissionOverwrite(view_channel=True,connect=False),
                                    closemod:PermissionOverwrite(view_channel=True,kick_members=True),
                                    closeban:PermissionOverwrite(view_channel=False)
                        }

                        for member in members:
                            if member.team == "dark":
                                user = inter.guild.get_member(member.discord_id)
                                overwrites[user] = PermissionOverwrite(
                                    connect=False
                                )

                        light = await inter.guild.create_voice_channel(
                                name='🌕・Силы света',
                                category=category,
                                overwrites=overwrites
                        )                            
                        overwrites = {
                                    everyone:PermissionOverwrite(view_channel=True,connect=False),
                                    closemod:PermissionOverwrite(view_channel=True,kick_members=True),
                                    closeban:PermissionOverwrite(view_channel=False)
                        }

                        for member in members:
                            if member.team == "light":
                                user = inter.guild.get_member(member.discord_id)
                                overwrites[user] = PermissionOverwrite(
                                    connect=False
                                )
                        dark = await inter.guild.create_voice_channel(
                                name='🌑・Силы тьмы',
                                category=category,
                                overwrites={
                                    everyone:PermissionOverwrite(view_channel=True,connect=False),
                                    closemod:PermissionOverwrite(view_channel=True,kick_members=True),
                                    closeban:PermissionOverwrite(view_channel=False)
                                }

                        )
                        password = random.randint(1,4)
                        name = f"DOTA2RU{random.randint(1,4)}"
                        embed = dis.Embed.from_dict(
                            {
                                "title": "Dota 2 ・ Информация ᅠ  ᅠ  ᅠ  ᅠ  ᅠ  ᅠ",
                                "description": "**Готовность:** не создано \n**Название лобби:** " + name + "\n**Пароль:** " + password + "\n**Регион:** Стокгольм",
                                "color": 3092790
                            }                            
                        )
                        row = dis.ui.ActionRow.with_message_components()
                        row.add_button(
                            style=dis.ButtonStyle.success,
                            label="Сообщить о готовности лобби",
                            custom_id=f"lobbycreated.{close_id}"
                        )
                        await lobby.send(embed,components=row)
                        
def setup(bot:CloseBot):
    bot.add_cog(CloseStartButton(bot))