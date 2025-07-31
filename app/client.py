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

    def launch(self):
        self.run(self.settings.TOKEN)