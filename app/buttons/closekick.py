import disnake as dis
import disnake
from disnake.ext import commands
from disnake.ext.commands import Cog

from app.client import CloseBot

class CloseKickButton(Cog):
    def __init__(self,bot:CloseBot):
        self.bot = bot
        super().__init__()


    @commands.Cog.listener()
    async def on_button_click(self,inter:dis.MessageInteraction):
        if inter.component.custom_id.startswith("closeremove"):
            await inter.response.defer(with_message=True,ephemeral=True)
            raw_data = inter.component.custom_id.split(".")
            close_id = int(raw_data[-1])
            close = await self.bot.clm.getCloseById(close_id)
            members = await self.bot.clm.get_members(close_id)
            if inter.guild.get_role(self.bot.settings.roles.closemod) in inter.author.roles:
                if inter.author.id == close.creator:
                    if len(members) > 0:
                        select = dis.ui.StringSelect(custom_id=f"closekick.{close_id}",placeholder="Выбери участника",max_values=1)
                        for member in members:
                            user = inter.guild.get_member(member.discord_id)
                            match member.team:
                                case "dark":
                                    team = self.bot.settings.emojis.dark
                                case "light":
                                    team = self.bot.settings.emojis.light 
                            select.add_option(
                                label=user.display_name,
                                value=f'{member.discord_id}.{close_id}',
                                description=f"{team} позиция:{self.bot.settings.line[str(member.pos)]}"
                            )
                        await inter.edit_original_message(components=[select])
                    else:
                        await inter.edit_original_message("## Нету участников клоза")
                else:
                    await inter.edit_original_message("## Вы не создатель клоза")
            else:
                await inter.edit_original_message("## Вы не клозмод")

def setup(bot:CloseBot):
    bot.add_cog(CloseKickButton(bot))