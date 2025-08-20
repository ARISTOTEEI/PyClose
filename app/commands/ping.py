import disnake as dis

from disnake.ext.commands import Cog
from disnake.ext import commands

from app.client import CloseBot

class PingCommand(Cog):
    def __init__(self,bot:CloseBot):
        self.bot = bot
        super().__init__()

    @commands.slash_command(name="ping")
    async def ping_command(self,inter:dis.AppCmdInter):
        await inter.response.send_message(f"My ping is {(self.bot.latency)}")

def setup(bot:CloseBot):
    bot.add_cog(PingCommand(bot))