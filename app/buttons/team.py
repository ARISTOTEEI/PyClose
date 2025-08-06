import disnake as dis
from disnake.ext import commands
from disnake.ext.commands import Cog
from app.client import CloseBot
from app.entryMessage import update_message
from app.utils.schemas import *

class TeamButton(Cog):
    def __init__(self,bot:CloseBot):
        self.bot = bot
        super().__init__()

    @commands.Cog.listener()
    async def on_button_click(self,inter:dis.MessageInteraction):
        component = inter.component
        raw_data = component.custom_id.split('.')
        if raw_data[0] == "team":
            embed = dis.Embed(title="Выбери позицию")
            row = dis.ui.ActionRow.with_message_components()
            members = await self.bot.clm.get_members(raw_data[-1])
            row.add_button(
                style=dis.ButtonStyle.grey,
                custom_id=f"pos.1.{raw_data[1]}.{raw_data[2]}",
                emoji=self.bot.settings.emojis.Knife,
                disabled=next((True for x in members if x.pos == 1 and x.team == raw_data[1]),False)
            )
            row.add_button(
                style=dis.ButtonStyle.grey,
                custom_id=f"pos.2.{raw_data[1]}.{raw_data[2]}",
                emoji=self.bot.settings.emojis.Onion,
                disabled=next((True for x in members if x.pos == 2 and x.team == raw_data[1]),False)
            )
            row.add_button(
                style=dis.ButtonStyle.grey,
                custom_id=f"pos.3.{raw_data[1]}.{raw_data[2]}",
                emoji=self.bot.settings.emojis.Security,
                disabled=next((True for x in members if x.pos == 3 and x.team == raw_data[1]),False)
            )
            row.add_button(
                style=dis.ButtonStyle.grey,
                custom_id=f"pos.4.{raw_data[1]}.{raw_data[2]}",
                emoji=self.bot.settings.emojis.Conhand,
                disabled=next((True for x in members if x.pos == 4 and x.team == raw_data[1]),False)
            )
            row.add_button(
                style=dis.ButtonStyle.grey,
                custom_id=f"pos.5.{raw_data[1]}.{raw_data[2]}",
                emoji=self.bot.settings.emojis.Conhands,
                disabled = next((True for x in members if x.pos == 1 and x.team == raw_data[1]),False)
            )
            await inter.response.send_message(components=row,embed=embed,ephemeral=True)
        if raw_data[0] == "pos":
            member = CloseMemberCreateSchema(
                discord_id=inter.author.id,
                pos=int(raw_data[1]),
                team=raw_data[2],
                close_id=raw_data[-1]
            )
            close = await self.bot.clm.getCloseById(raw_data[-1])
            await self.bot.clm.append_member(raw_data[-1],member)
            embed = await update_message(self.bot,raw_data[-1])
            message = await inter.guild.get_channel(close.messagechannel).fetch_message(close.message)
            await message.edit(embed = embed)
            await inter.response.send_message("Вы успешно записались!!!",ephemeral=True)




def setup(bot:CloseBot):
    bot.add_cog(TeamButton(bot))