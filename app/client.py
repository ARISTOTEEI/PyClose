import disnake
from disnake.ext.commands import InteractionBot
from utils import *
from .config import TOKEN

class CloseBot(InteractionBot):
    def __init__(self):
        super().__init__(intents=disnake.Intents.all())
        self.async_sessionmaker = database.async_session
        self.load_extensions(r"app\commands")
        self.load_extensions(r"app\events")
        self.load_extensions(r"app\buttons")
        self.load_extensions(r"app\menu")

    async def on_ready(self):
        print(f"Bot {self.user.display_name} is online!")

    def launch(self):
        self.run(TOKEN)