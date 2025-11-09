from sqlalchemy import String, DateTime, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime, timezone
from typing import Optional

class Base(DeclarativeBase):
    pass

class Incident(Base):
    """
    Доменный класс для отражения инцидента из БД.

    Абстрагируется от типа БД за счёт SQLAlchemy.
    """
    __tablename__ = 'incidents'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False)
    source: Mapped[str] = mapped_column(String(20), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    def __init__(
        self, 
        text: str, 
        status: str, 
        source: str, 
        created_at: Optional[datetime] = None
    ):
        super().__init__()
        self.text = text
        self.status = status
        self.source = source
        self.created_at = created_at or datetime.now(timezone.utc)

    def __repr__(self) -> str:
        return f"Incident(id={self.id}, status='{self.status}', source='{self.source}')"