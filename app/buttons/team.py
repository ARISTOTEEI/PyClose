import disnake as dis
from disnake.ext import commands
from disnake.ext.commands import Cog
from app.client import CloseBot
from app.entryMessage import update_message
from app.utils.schemas import *


class TeamButton(Cog):
    def __init__(self, bot: CloseBot):
        self.bot = bot
        super().__init__()

    @commands.Cog.listener()
    async def on_button_click(self, inter: dis.MessageInteraction):
        component = inter.component
        raw_data = component.custom_id.split('.')
        button = raw_data[0]
        if button == "team":
            team = raw_data[1]
            close_id = raw_data[-1]
            embed = dis.Embed(title="Выбери позицию")
            row = dis.ui.ActionRow.with_message_components()
            members = await self.bot.clm.get_members(int(close_id))

            row.add_button(
                style=dis.ButtonStyle.grey,
                custom_id=f"pos.1.{team}.{close_id}",
                emoji=self.bot.settings.emojis.Knife,
                disabled=next((True for x in members if x.pos ==
                              1 and x.team == team), False)
            )
            row.add_button(
                style=dis.ButtonStyle.grey,
                custom_id=f"pos.2.{team}.{close_id}",
                emoji=self.bot.settings.emojis.Onion,
                disabled=next((True for x in members if x.pos ==
                              2 and x.team == team), False)
            )
            row.add_button(
                style=dis.ButtonStyle.grey,
                custom_id=f"pos.3.{team}.{close_id}",
                emoji=self.bot.settings.emojis.Security,
                disabled=next((True for x in members if x.pos ==
                              3 and x.team == team), False)
            )
            row.add_button(
                style=dis.ButtonStyle.grey,
                custom_id=f"pos.4.{team}.{close_id}",
                emoji=self.bot.settings.emojis.Conhand,
                disabled=next((True for x in members if x.pos ==
                              4 and x.team == team), False)
            )
            row.add_button(
                style=dis.ButtonStyle.grey,
                custom_id=f"pos.5.{team}.{close_id}",
                emoji=self.bot.settings.emojis.Conhands,
                disabled=next((True for x in members if x.pos ==
                              5 and x.team == team), False)
            )
            await inter.response.send_message(components=row, embed=embed, ephemeral=True)
        if button == "pos":
            member = await self.bot.clm.get_member(inter.author.id)
            close_id = raw_data[-1]
            pos = raw_data[1]
            team = raw_data[2]
            if member is None:
                member = CloseMemberCreateSchema(
                    discord_id=inter.author.id,
                    pos=int(pos),
                    team=team,
                    close_id=close_id
                )
                await self.bot.clm.append_member(int(close_id), member)
            else:
                await self.bot.clm.edit_member(inter.author.id, int(pos), team)

            close = await self.bot.clm.getCloseById(int(close_id))
            embed = await update_message(self.bot, int(close_id))
            message = await inter.guild.get_channel(close.messagechannel).fetch_message(close.message)
            await message.edit(embed=embed)
            await inter.response.edit_message("Вы успешно записались!!!", components=[], embed=None)


def setup(bot: CloseBot):
    bot.add_cog(TeamButton(bot))
