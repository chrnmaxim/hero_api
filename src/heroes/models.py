from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class HeroModel(Base):
    """Модель супер-героев."""

    __tablename__ = "heroes"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(comment="Имя", index=True)
    powerstats: Mapped[dict[str, int]] = mapped_column(JSONB, comment="Характеристики")
    biography: Mapped[dict[str, str]] = mapped_column(JSONB, comment="Биография")
    appearance: Mapped[dict[str, str | list[str]]] = mapped_column(
        JSONB, comment="Внешность"
    )
    work: Mapped[dict[str, str]] = mapped_column(JSONB, comment="Работа")
    connections: Mapped[dict[str, str]] = mapped_column(JSONB, comment="Связи")
    image: Mapped[str] = mapped_column(JSONB, comment="Ссылка на изображение")
