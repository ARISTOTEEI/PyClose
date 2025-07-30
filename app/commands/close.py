import disnake as dis
from disnake.ext.commands import Cog, Param, InteractionBot
from disnake.ext import commands
from disnake import PermissionOverwrite
from ..client import CloseBot
from ..closemanager import CloseSource

class CloseCommand(Cog):
    def __init__(self,bot:CloseBot) -> None:
        self.bot = bot
        super().__init__()

    @commands.slash_command(name="close",description="Create close Dota 2")
    async def close_command(self,inter:dis.AppCmdInter,type:str = Param(choices={"random":"random","team":"team"})):
        if not(inter.guild):
            await inter.response.send_message("Не используйте в личных сообщениях",ephemeral=True)
            return
        closemod = inter.guild.get_role(self.bot.settings.roles.closemod)
        
        if closemod not in inter.author.roles:
            await inter.response.send_message("У вас нету роли клозмейкера",ephemeral=True)
            return
        
        if (self.bot.clm.getCloseByCreator(inter.author.id)):
            await inter.response.send_message("У вас уже запущен клоз",ephemeral=True)
            return
        
        closeban = inter.guild.get_role(self.bot.settings.roles.closeban)
        everyone = inter.guild.default_role

        category = await inter.guild.create_category(
            name="Close",
            overwrites={
                closeban:PermissionOverwrite(view_channel=False)
            }
        )

        managechannel = await inter.guild.create_text_channel(
            name = "Управление",
            category=category,
            overwrites={
                everyone:PermissionOverwrite(view_channel=False),
                closemod:PermissionOverwrite(view_channel=True),
                closeban:PermissionOverwrite(view_channel=False)
            }
        )

        waitingchannel = await inter.guild.create_voice_channel(
           name="Ожидание", 
        )

        await inter.response.send_message("Клоз создан",ephemeral=True)


def setup(bot:InteractionBot):
    bot.add_cog(CloseCommand(bot))

