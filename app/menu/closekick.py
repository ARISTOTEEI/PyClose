import disnake
import disnake as dis
from disnake.ext import commands
from disnake.ext.commands import Cog

from app.client import CloseBot
from app.entryMessage import update_message

class CloseKickSelect(Cog):
    def __init__(self,bot:CloseBot):
        self.bot = bot
        super().__init__()

    @commands.Cog.listener()
    async def on_dropdown(self,inter:dis.MessageInteraction):
        if inter.component.custom_id.startswith("closekick"):
            raw_data = inter.component.custom_id.split(".")
            close_id = int(raw_data[-1])
            discord_i = int(raw_data[0])
            if inter.guild.get_role(self.bot.settings.roles.closemod) in inter.author.roles:
                close = await self.bot.clm.getCloseById(close_id)
                await self.bot.clm.delete_member(discord_i)
                await inter.response.send_message("## Вы успешно кикнули человека с клоза",ephemeral=True)
                embed = await update_message(self.bot,close_id)
                message = await inter.guild.get_channel(close.messagechannel).fetch_message(close.message)
                await message.edit(embed = embed)

def setup(bot:CloseBot):
    bot.add_cog(CloseKickSelect(bot))
    