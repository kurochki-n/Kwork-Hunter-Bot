from sqlalchemy import BigInteger, ARRAY, LargeBinary, String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[str] = mapped_column(String, nullable=True)
    first_name: Mapped[str] = mapped_column(String, nullable=True)
    last_name: Mapped[str] = mapped_column(String, nullable=True)
    language_code: Mapped[str] = mapped_column(String, nullable=False)
    is_bot: Mapped[bool] = mapped_column(Boolean, nullable=False)
    is_premium: Mapped[bool] = mapped_column(Boolean, nullable=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, nullable=False)
    
    kwork_session: Mapped["KworkSession"] = relationship("KworkSession", back_populates="user", foreign_keys="KworkSession.user_id")
    
    
class KworkSession(Base):
    __tablename__ = "kwork_sessions"
    
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"), primary_key=True)
    login: Mapped[LargeBinary] = mapped_column(LargeBinary(), nullable=True)
    password: Mapped[LargeBinary] = mapped_column(LargeBinary(), nullable=True)
    cookie: Mapped[LargeBinary] = mapped_column(LargeBinary(), nullable=True)
    last_projects: Mapped[list[BigInteger]] = mapped_column(ARRAY(BigInteger), nullable=True, default=[])
    
    user: Mapped["User"] = relationship("User", back_populates="kwork_session", foreign_keys=[user_id])
