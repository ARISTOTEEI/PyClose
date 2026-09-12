import disnake as dis
from disnake.ext import commands
from disnake.ext.commands import Cog

from app.client import CloseBot
from app.entrymessage import update_message, update_v2_message


class CloseExitButton(Cog):
    def __init__(self, bot: CloseBot):
        self.bot = bot
        super().__init__()

    @commands.Cog.listener()
    async def on_button_click(self, inter: dis.MessageInteraction):
        if inter.component.custom_id.startswith("closeexit"):
            raw_data = inter.component.custom_id.split(".")
            close_id = int(raw_data[1])
            member = await self.bot.clm.get_member(inter.author.id)
            if member:
                await inter.response.send_message("## Вы успешно вышли из записи на клоз", ephemeral=True)
                await self.bot.clm.delete_member(inter.author.id)
                close = await self.bot.clm.getCloseById(close_id)
                message = await inter.guild.get_channel(close.messagechannel).fetch_message(close.message)
                if member.team == "random":
                    container = await update_v2_message(self.bot,close_id)
                    await message.edit(components=container)
                else:
                    embed = await update_message(self.bot, close_id)
                    await message.edit(embed=embed)
            else:
                await inter.response.send_message("## Вы не учавствуете в клозе", ephemeral=True)


def setup(bot: CloseBot):
    bot.add_cog(CloseExitButton(bot))
