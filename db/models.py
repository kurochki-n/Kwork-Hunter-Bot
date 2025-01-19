from sqlalchemy import BigInteger, ARRAY, LargeBinary
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[BigInteger] = mapped_column(BigInteger, primary_key=True)
    kwork_login: Mapped[LargeBinary] = mapped_column(LargeBinary(), nullable=True)
    kwork_password: Mapped[LargeBinary] = mapped_column(LargeBinary(), nullable=True)
    kwork_cookie: Mapped[LargeBinary] = mapped_column(LargeBinary(), nullable=True)
    last_projects: Mapped[list[BigInteger]] = mapped_column(ARRAY(BigInteger), nullable=True, default=[])

