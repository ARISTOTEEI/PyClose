from pydantic import BaseModel, Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

roles = {
    "closemod": 1160124199902396458,
    "closeban": 1160128387390636085,
    "closenotify": 1160124206177079357
}
    
channels = {
    "log_channel": 1011561762417557576,
    "notification_channel": 1011561762417557576,
    "win_channel": 1011561762417557576
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
    
    @model_validator(mode="after")
    def validate_roles(self) -> "SRoles":
        for name,value in self:
            if value == 0:
                raise ValueError(f"Bad Config roles, {name} is {value}")
        return self

class SChannels(BaseModel):
    log_channel: int | None
    notification_channel: int
    win_channel: int

    @model_validator(mode="after")
    def validate_channels(self) -> "SChannels":
        for name,value in self:
            if value == 0:
                raise ValueError(f"Bad Config channels, {name} is {value}")
        return self

class SEmojis(BaseModel):
    Knife: str
    Onion: str
    Security: str
    Conhand: str
    Conhands: str
    dark: str
    light: str

    @model_validator(mode="after")
    def validate_emojis(self) -> "SEmojis":
        for name,value in self:
            if value == "":
                raise ValueError(f"Bad Config channels, {name} is {value}")
        return self

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

    TOKEN: str

    @property
    def DATABASE_url_asyncpg(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(env_file="app/.env")


settings = Settings()
