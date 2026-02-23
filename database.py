from sqlalchemy.orm import DeclarativeBase, Mapped , mapped_column
from sqlalchemy import String

class Base(DeclarativeBase):
    pass

#map users table to User class 
class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    location: Mapped[str] = mapped_column(String(100))
