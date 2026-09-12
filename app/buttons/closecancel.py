import disnake as dis
from disnake.ext import commands
from disnake.ext.commands import Cog

from app.client import CloseBot


class CloseCancelButton(Cog):
    def __init__(self, bot: CloseBot):
        self.bot = bot
        super().__init__()

    @commands.Cog.listener()
    async def on_button_click(self, inter: dis.MessageInteraction):
        if inter.component.custom_id.startswith("closecancel"):
            component = inter.component
            raw_data = component.custom_id.split(".")
            if inter.guild.get_role(self.bot.settings.roles.closemod) in inter.author.roles:
                close = await self.bot.clm.getCloseById(int(raw_data[-1]))
                if close.creator == inter.author.id:
                    await inter.response.send_message("## Вы успешно удалили клоз", ephemeral=True)
                    category = inter.guild.get_channel(
                        close.managechannel).category
                    for channel in category.channels:
                        await channel.delete()
                    await category.delete()
                    await self.bot.clm.delete_close(close.creator)
                else:
                    await inter.response.send_message("## Вы не являетесь создателем клоза", ephemeral=True)
            else:
                await inter.response.send_message("## Вы не являетесь клозмодом", ephemeral=True)


def setup(bot: CloseBot):
    bot.add_cog(CloseCancelButton(bot))
