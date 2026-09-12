import datetime

import disnake as dis
from disnake.ext import commands
from disnake.ext.commands import Cog

from app.client import CloseBot
from app.utils.schemas import CloseUpdateSchema


class CloseCallButton(Cog):
    def __init__(self, bot: CloseBot):
        self.bot = bot
        super().__init__()

    @commands.Cog.listener()
    async def on_button_click(self, inter: dis.MessageInteraction):
        if inter.component.custom_id.startswith("closecall"):
            if inter.guild.get_role(self.bot.settings.roles.closemod) in inter.author.roles:
                raw_data = inter.component.custom_id.split(".")
                close_id = int(raw_data[-1])
                close = await self.bot.clm.getCloseById(close_id)
                if inter.author.id == close.creator:
                    await inter.response.defer(with_message=True, ephemeral=True)
                    time = datetime.datetime.fromtimestamp(close.lastcall if close.lastcall != None else 0)
                    now = datetime.datetime.now()
                    timeout = datetime.timedelta(minutes=5)
                    if (now - time).total_seconds() >= timeout.total_seconds():
                        members = await self.bot.clm.get_members(close_id)
                        mentions = ""
                        poses = [2, 2, 2, 2, 2]
                        for member in members:
                            poses[member.pos-1] -= 1
                        for index, pos in enumerate(poses, 1):
                            mentions += f" +{pos} {self.bot.settings.line[str(index)]}"
                        role = inter.guild.get_role(
                            self.bot.settings.roles.closenotify)
                        await inter.guild.get_channel(close.managechannel).send(f"{role.mention} {mentions}")
                        await inter.edit_original_message('## Вы успешно позвали людей на клоз.')
                        update = CloseUpdateSchema(lastcall=int(
                            now.timestamp()), message=close.message)
                        await self.bot.clm.update_close(close_id, update)
                    else:
                        await inter.edit_original_message("## Вы не можете звать людей на клоз чаще чем раз в 5 минут.")
                else:
                    await inter.response.send_message("## Вы не являетесь создателем клоза", ephemeral=True)
            else:
                await inter.response.send_message("## Вы не являетесь клозмодом", ephemeral=True)


def setup(bot: CloseBot):
    bot.add_cog(CloseCallButton(bot))
