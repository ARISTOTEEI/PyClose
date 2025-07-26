from pydantic_settings import BaseSettings,SettingsConfigDict

class Settings(BaseSettings):
    DB_USER:str
    DB_PASS:str
    DB_NAME:str
    DB_HOST:str
    DB_PORT:str
    TOKEN:str

    @property
    def DATABASE_url_asyncpg(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
