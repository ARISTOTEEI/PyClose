from sqlalchemy import Table,Column,Integer,MetaData
from sqlalchemy.orm import mapped_column
from database import Base

class Close(Base):
    __tablename__ = "close"
    id = mapped_column