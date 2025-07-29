import disnake
from disnake.ext.commands import InteractionBot
from ..utils import *

class CloseBot(InteractionBot):
    def __init__(self):
        super().__init__(intents=disnake.Intents.all())
        self.async_sessionmaker = database.async_session
        self.load_extensions("app.commands")
        self.load_extensions("app.events")
        self.load_extensions("buttons")
        self.load_extensions("menu")

    async def on_ready(self):
        print(f"Bot {self.user.display_name} is online!")
        async with self.async_sessionmaker() as session:
            await session.