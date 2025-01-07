from sqlalchemy import BigInteger, String, ARRAY, Integer
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    kwork_login: Mapped[str] = mapped_column(String(32), nullable=True)
    kwork_password: Mapped[str] = mapped_column(String(32), nullable=True)
    kwork_cookie: Mapped[str] = mapped_column(String(1024), nullable=True)
    last_projects: Mapped[list[int]] = mapped_column(ARRAY(Integer), nullable=True, default=[])


