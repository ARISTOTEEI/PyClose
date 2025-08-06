import disnake as dis
from disnake.ext import commands
from disnake.ext.commands import Cog
from app.client import CloseBot

class TeamButton(Cog):
    def __init__(self,bot:CloseBot):
        self.bot = bot
        super().__init__()

    @commands.Cog.listener()
    async def on_button_click(self,inter:dis.MessageInteraction):
        component = inter.component
        raw_data = component.custom_id.split('.')
        if raw_data[0] == "team":
            embed = dis.Embed(title="Выбери позицию")
            row = dis.ui.ActionRow.with_message_components()
            row.add_button(
                style=dis.ButtonStyle.grey,
                custom_id=f"pos.1.{raw_data[1]}.{raw_data[2]}",
                emoji=self.bot.settings.emojis.Knife
            )
            row.add_button(
                style=dis.ButtonStyle.grey,
                custom_id=f"pos.2.{raw_data[1]}.{raw_data[2]}",
                emoji=self.bot.settings.emojis.Onion
            )
            row.add_button(
                style=dis.ButtonStyle.grey,
                custom_id=f"pos.3.{raw_data[1]}.{raw_data[2]}",
                emoji=self.bot.settings.emojis.Security
            )
            row.add_button(
                style=dis.ButtonStyle.grey,
                custom_id=f"pos.4.{raw_data[1]}.{raw_data[2]}",
                emoji=self.bot.settings.emojis.Conhand
            )
            row.add_button(
                style=dis.ButtonStyle.grey,
                custom_id=f"pos.5.{raw_data[1]}.{raw_data[2]}",
                emoji=self.bot.settings.emojis.Conhands
            )
            await inter.response.send_message(components=row,embed=embed,ephemeral=True)
        if raw_data[0] == "pos":
            pass


def setup(bot:CloseBot):
    bot.add_cog(TeamButton(bot))