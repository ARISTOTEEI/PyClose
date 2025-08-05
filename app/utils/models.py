from sqlalchemy import Identity,ForeignKey,BigInteger,text
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.orm import mapped_column,Mapped
from app.utils.database import Base
from enum import Enum

class CloseType(str,Enum):
    TEAM = 'team'
    RANDOM = 'random'

class TeamType(str,Enum):
    DARK = 'dark'
    LIGHT = 'light'

class CloseORM(Base):
    __tablename__ = "close"
    id: Mapped[int] = mapped_column(primary_key=True,server_default=Identity())
    type: Mapped[CloseType] = mapped_column(SQLEnum(CloseType))
    managechannel: Mapped[int] = mapped_column(BigInteger) # Это управление клозом
    waitingchannel: Mapped[int] = mapped_column(BigInteger) # Это голосовой канал ожидания
    creator:Mapped[int] = mapped_column(BigInteger)
    lastcall:Mapped[int | None] = mapped_column(default=None) # Время последнего вызова на клоз
    message:Mapped[int | None] = mapped_column(BigInteger,default=None) # Это сообщение с записью на клоз
    messagechannel:Mapped[int] = mapped_column(BigInteger) # Это канал с записью на клоз
    members: Mapped[list["CloseMemberORM"]] = relationship("CloseMemberORM", lazy="selectin",back_populates="close",cascade="all, delete-orphan",)  # Автоматическое удаление связанных записейpassive_deletes=True  # Оптимизация для PostgreSQL

class CloseMemberORM(Base):
    __tablename__ = 'closemember'
    id:Mapped[int] = mapped_column(primary_key=True,server_default=Identity())
    discord_id:Mapped[int] = mapped_column(BigInteger)
    pos: Mapped[int]
    team: Mapped[TeamType] = mapped_column(SQLEnum(TeamType))
    close_id: Mapped[int] = mapped_column(ForeignKey("close.id"),nullable=False)
    close: Mapped["CloseORM"] = relationship("CloseORM", back_populates="members")

class UserORM(Base):
    __tablename__ = "user"
    userid:Mapped[int] = mapped_column(BigInteger,primary_key=True)
    pos1games: Mapped[int] = mapped_column(default=0)
    pos1wins: Mapped[int] = mapped_column(default=0)
    pos2games: Mapped[int] = mapped_column(default=0)
    pos2wins: Mapped[int] = mapped_column(default=0)
    pos3games: Mapped[int] = mapped_column(default=0)
    pos3wins: Mapped[int] = mapped_column(default=0)
    pos4games: Mapped[int] = mapped_column(default=0)
    pos4wins: Mapped[int] = mapped_column(default=0)
    pos5games: Mapped[int] = mapped_column(default=0)
    pos5wins: Mapped[int] = mapped_column(default=0)