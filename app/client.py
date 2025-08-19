import disnake as dis
import disnake
from disnake.ext.commands import InteractionBot
from app.config import settings
from app.closemanager import CloseManager
from app.utils.database import async_session


class CloseBot(InteractionBot):
    def __init__(self):
        super().__init__(intents=disnake.Intents.all())
        self.clm = CloseManager(async_session)
        self.settings = settings
        self.async_sessionmaker = async_session
        self.load_extensions(r"app\commands")
        self.load_extensions(r"app\events")
        self.load_extensions(r"app\buttons")
        self.load_extensions(r"app\menu")

    async def on_ready(self):
        print(f"Bot {self.user.display_name} is online!")
        await self.change_presence(activity=dis.Game(f"with {self.owner.name}"), status=dis.Status.idle)

    async def on_button_click(self, inter: disnake.MessageInteraction):
        if inter.guild.get_role(self.settings.roles.closeban) in inter.author.roles:
            return await inter.response.send_message("У вас клозбан!", ephemeral=True)

    def launch(self):
        self.run(self.settings.TOKEN)
