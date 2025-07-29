from pydantic_settings import BaseSettings,SettingsConfigDict

class Settings(BaseSettings):
    DB_USER:str
    DB_PASS:str
    DB_NAME:str
    DB_HOST:str
    DB_PORT:str

    @property
    def DATABASE_url_asyncpg(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    model_config = SettingsConfigDict(env_file="app/.env")

settings = Settings()

TOKEN = "MTAwMjIyMTYxMTM4NDA2MjAyNA.GNmHdQ.qXaw-2BZfGS4ZbZxfFbenjP6GxjAiCaGNuUdGw"

roles = {
    "closemod":1011684141600878714,
    "closeban":1231
}

channels = {
    "logs":13213,
    "notif":1231,
    "winnerch":1231
}

name_channel = {
    "category_name":"",
    "manage_name":"",
    "wait_name":"",
    "watch_name":"",
    "ligh_name":"",
    "dark_name":"",
}

emojis = {
    "Knife": "<:freeiconsword842082:1393537105208152155>",
    "Onion": "<:freeiconbow1885298:1393537102511083570>",
    "Security": "<:freeiconshield3077175:1393537099252367390>",
    "Conhand": "<:freeiconhand1534403:1393537096328679557>",
    "Conhands": "<:freeiconheart3477186:1393537093791387759>",
    "dark": "🌑",
    "light": "🌕"
}

line = {
    "1":"Лёгкая",
    "2":"Центр",
    "3":"Сложная",
    "4":"Частичная поддержка",
    "5":"Полная поддержка"
}

