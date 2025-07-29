import disnake as dis
from disnake.ext.commands import Cog, Param, InteractionBot
from disnake.ext import commands
from ..config import roles
from ..closemanager import Close

class CloseCommand(Cog):
    def __init__(self,bot:InteractionBot) -> None:
        self.bot = bot
        super().__init__()

    @commands.slash_command(name="close",description="Create close Dota 2")
    async def close_command(self,inter:dis.AppCmdInter,type:str = Param(choices={"random":"random","team":"team"})):
        if not(inter.guild):
            await inter.response.send_message("Не используйте в личных сообщениях",ephemeral=True)
            return
        closemod = inter.guild.get_role(roles.get("closemod"))
        if closemod not in inter.author.roles:
            await inter.response.send_message("У вас нету роли клозмейкера",ephemeral=True)
            return
        
        close = Close()

        # await close.create_close()
        
        if not(close.status):
            await inter.response.send_message("Ошибка создания клоза",ephemeral=True)
            return

        await inter.response.send_message("Клоз создан",ephemeral=True)


def setup(bot:InteractionBot):
    bot.add_cog(CloseCommand(bot))

