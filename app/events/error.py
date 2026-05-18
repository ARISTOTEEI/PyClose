import disnake as dis
from disnake.ext import commands
import disnake
from ..client import CloseBot

class ErrorEvent(commands.Cog):
    def __init__(self,bot:CloseBot):
        self.bot = bot
        super().__init__()
        
    @commands.Cog.listener(dis.Event.error)
    async def on_error(self,event,*args, **kwargs):
        if event == "on_button_click":
            inter:dis.MessageInteraction = args[0]
            await inter.response.send_message("Ошибка",ephemeral=True) 

def setup(bot:CloseBot):
    bot.add_cog(ErrorEvent(bot))