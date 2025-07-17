from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from src.database import SessionLocal


# MARK: Session
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    AsyncGenerator экземпляра `AsyncSession`.

    Сессия закрывается внутри контекстного менеджера автоматически.
    """

    async with SessionLocal() as session:
        try:
            yield session
        except Exception as ex:
            raise ex
