from sqlalchemy import BigInteger, ARRAY, LargeBinary
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    kwork_login: Mapped[str] = mapped_column(LargeBinary(), nullable=True)
    kwork_password: Mapped[str] = mapped_column(LargeBinary(), nullable=True)
    kwork_cookie: Mapped[str] = mapped_column(LargeBinary(), nullable=True)
    last_projects: Mapped[list[int]] = mapped_column(ARRAY(BigInteger), nullable=True, default=[])


