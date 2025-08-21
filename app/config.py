from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel, Field

roles = {
    "closemod": 0,
    "closeban": 0,
    "closenotify": 0
}

channels = {
    "log_channel": 0,
    "notification_channel": 0,
    "win_channel": 0
}

emojis = {
    "Knife": "",
    "Onion": "",
    "Security": "",
    "Conhand": "",
    "Conhands": "",
    "dark": "🌑",
    "light": "🌕"
}

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
        default="TOKEN")

    @property
    def DATABASE_url_asyncpg(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(env_file="app/.env")


settings = Settings()
