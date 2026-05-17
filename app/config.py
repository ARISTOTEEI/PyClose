from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel, Field
from disnake import PartialEmoji

roles = {
    "closemod": 1160124199902396458,
    "closeban": 1160128387390636085,
    "closenotify": 0
}

for i,b in roles.items():
    if b==0:
        raise Exception(f"bad config {i} is {b}")
    
channels = {
    "log_channel": 0,
    "notification_channel": 0,
    "win_channel": 0
}


### Emoji
###                 <name:id>
emojis = {
    "Knife": "<:Knife:1405556977014407168>",
    "Onion": "<:Onion:1405557001982967919>",
    "Security": "<:Security:1405557022908350654>",
    "Conhand": "<:Conhand:1405557053618913320>",
    "Conhands": "<:Conhands:1405557077807468585>",
    "dark": "🌑",
    "light": "🌕"
}

for i,b in emojis.items():
    if b=="":
        raise Exception(f"bad config {i} is '{b}' ")

line = {
    "1": "Лёгкая",
    "2": "Центр",
    "3": "Сложная",
    "4": "Частичная поддержка",
    "5": "Полная поддержка"
}


class SRoles(BaseModel):
    closemod: int
    closeban: int
    closenotify: int


class SChannels(BaseModel):
    log_channel: int | None
    notification_channel: int
    win_channel: int


class SEmojis(BaseModel):
    Knife: str
    Onion: str
    Security: str
    Conhand: str
    Conhands: str
    dark: str
    light: str


class Settings(BaseSettings):
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    DB_HOST: str
    DB_PORT: str

    channels: SChannels = Field(default=SChannels(**channels))
    roles: SRoles = Field(default=SRoles(**roles))
    emojis: SEmojis = Field(default=SEmojis(**emojis))
    line: dict = Field(default=line)

    TOKEN: str = Field(
        default="MTAwMjIyMTYxMTM4NDA2MjAyNA.GxZaXB.xdutByU6YRyolA36qqmH0wGPhRLj3R9JzZ94aI")

    @property
    def DATABASE_url_asyncpg(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(env_file="app/.env")


settings = Settings()
