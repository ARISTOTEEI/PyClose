from sqlalchemy import Identity,ForeignKey,BigInteger
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import mapped_column,Mapped
from datetime import datetime,timezone
from database import Base
from enum import Enum

class CloseType(str,Enum):
    COMMAND = 'command'
    RANDOM = 'random'

class Close(Base):
    __tablename__ = "close"
    id: Mapped[int] = mapped_column(primary_key=True,server_default=Identity())
    type: Mapped[CloseType] = mapped_column(SQLEnum(CloseType))
    managechannel: Mapped[int] = mapped_column(BigInteger)
    waitingchannel: Mapped[int] = mapped_column(BigInteger)
    creator:Mapped[int] = mapped_column(BigInteger)
    create_at:Mapped[datetime] = mapped_column(default=lambda:datetime.now(timezone.utc))
    lastcall:Mapped[int] = mapped_column()
    message:Mapped[int] = mapped_column(BigInteger)
    messagechannel:Mapped[int] = mapped_column(BigInteger)

class CloseMembers(Base):
    __tablename__ = "closemember"
    userid:Mapped[int] = mapped_column(BigInteger)
    closeid:Mapped[int] = mapped_column(ForeignKey("close.id"),primary_key=True)
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