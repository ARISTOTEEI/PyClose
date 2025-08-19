import disnake
import disnake as dis
from disnake.ext import commands
from disnake.ext.commands import Cog

from app.client import CloseBot


class LobbyCreatedButton(Cog):
    def __init__(self, bot: CloseBot):
        self.bot = bot
        super().__init__()

    @commands.Cog.listener()
    async def on_button_click(self, inter: dis.MessageInteraction):
        if inter.component.custom_id.startswith('lobbycreated'):
            raw_data = inter.component.custom_id.split(".")
            close_id = int(raw_data[-1])
            members = await self.bot.clm.get_members(close_id)
            embed = dis.Embed.from_dict(
                {
                    "title": "Dota 2 ・ Информация ᅠ  ᅠ  ᅠ  ᅠ  ᅠ  ᅠ",
                    "description": inter.message.embeds[0].description.replace("**Готовность:** не создано", "**Готовность:** создано"),
                    "color": 3092790
                }
            )
            await inter.response.edit_message(embed=embed, components=None)
            mentions = ""
            for member in members:
                user = inter.guild.get_member(member.discord_id)
                mentions += f"{user.mention} "
            await inter.channel.send(mentions+"лобби создано!")


def setup(bot: CloseBot):
    bot.add_cog(LobbyCreatedButton(bot))
