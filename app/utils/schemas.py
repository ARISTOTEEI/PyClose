from sqlalchemy import Identity,ForeignKey,BigInteger,text
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import mapped_column,Mapped
from datetime import datetime,timezone
from app.utils.database import Base
from enum import Enum

class CloseType(str,Enum):
    COMMAND = 'command'
    RANDOM = 'random'

class Closes(Base):
    __tablename__ = "close"
    id: Mapped[int] = mapped_column(primary_key=True,server_default=Identity())
    type: Mapped[CloseType] = mapped_column(SQLEnum(CloseType))
    managechannel: Mapped[int] = mapped_column(BigInteger) # Это управление клозом
    waitingchannel: Mapped[int] = mapped_column(BigInteger) # Это голосовой канал ожидания
    creator:Mapped[int] = mapped_column(BigInteger)
    lastcall:Mapped[int | None] = mapped_column(default=None) # Время последнего вызова на клоз
    message:Mapped[int] = mapped_column(BigInteger) # Это сообщение с записью на клоз
    messagechannel:Mapped[int] = mapped_column(BigInteger) # Это канал с записью на клоз

class CloseMembers(Base):
    __tablename__ = "closemember"
    userid:Mapped[int] = mapped_column(BigInteger)
    closeid:Mapped[int | None] = mapped_column(ForeignKey("close.id"),default=None,primary_key=True)
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