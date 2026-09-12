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
            close = await self.bot.clm.getCloseById(close_id)
            if inter.guild.get_role(self.bot.settings.roles.closemod) in inter.author.roles:
                if close.creator == inter.author.id:
                    embed = dis.Embed.from_dict(
                        {
                            "title": "Dota 2 ・ Информация ᅠ  ᅠ  ᅠ  ᅠ  ᅠ  ᅠ",
                            "description": inter.message.embeds[0].description.replace("**Готовность:** не создано", "**Готовность:** создано"),
                            "color": 3092790
                        }
                    )
                    await inter.response.edit_message(embed=embed, components=None)
                    mentions = ""
                    for member in close.members:
                        user = inter.guild.get_member(member.discord_id)
                        mentions += f"{user.mention} "
                    await inter.channel.send(mentions+"лобби создано!")
                else:
                    await inter.response.send_message("## Вы не являетесь создателем клоза",ephemeral=True)
            else:
                await inter.response.send_message("## Вы не являетесь клозмодом",ephemeral=True)

def setup(bot: CloseBot):
    bot.add_cog(LobbyCreatedButton(bot))
