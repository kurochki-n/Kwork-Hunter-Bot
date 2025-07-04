import json

from sqlalchemy import BigInteger, LargeBinary, String, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[str] = mapped_column(String, nullable=True)
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=True)
    
    kwork_session: Mapped["KworkSession"] = relationship("KworkSession", back_populates="user", foreign_keys="KworkSession.user_id")
    
    
class KworkSession(Base):
    __tablename__ = "kwork_sessions"
    
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"), primary_key=True)
    login: Mapped[LargeBinary] = mapped_column(LargeBinary(), nullable=True)
    password: Mapped[LargeBinary] = mapped_column(LargeBinary(), nullable=True)
    cookie: Mapped[LargeBinary] = mapped_column(LargeBinary(), nullable=True)
    last_projects: Mapped[list[BigInteger]] = mapped_column(Text, nullable=True, default=json.dumps(list()))
    
    user: Mapped["User"] = relationship("User", back_populates="kwork_session", foreign_keys=[user_id])
