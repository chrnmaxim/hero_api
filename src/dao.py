from typing import Any, Generic, Literal, TypeVar, overload

from pydantic import BaseModel
from sqlalchemy import func, insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)


class BaseDAO(Generic[ModelType, CreateSchemaType]):
    """
    Основной класс интерфейсов для операция с моделям БД.

    Атрибуты класса:
        model (Type[ModelType]): модель SQLAlchemy.
    """

    model = Base

    # MARK: Bulk
    @overload
    @classmethod
    async def add_bulk(
        cls,
        session: AsyncSession,
        data: list[dict[str, Any]],
        returning: Literal[True],
    ) -> list[ModelType]: ...

    @overload
    @classmethod
    async def add_bulk(
        cls,
        session: AsyncSession,
        data: list[dict[str, Any]],
        returning: Literal[False] = False,
    ) -> None: ...

    @classmethod
    async def add_bulk(
        cls,
        session: AsyncSession,
        data: list[dict[str, Any]],
        returning: bool = False,
    ) -> list[ModelType] | None:
        """
        Добавить несколько записей в текущую сессию.

        Args:
            session(AsyncSession): асинхронная сессия SQLAlchemy.
            data(list[dict[str, Any]]): данные для добавления.
            returning(bool = True): возвращать ли все поля созданных моделей.

        Returns:
            list[ModelType]|None): созданные экземпляры модели или `None`.
        """

        stmt = insert(cls.model)
        if returning:
            stmt = stmt.returning(cls.model)
            result = await session.execute(stmt, data)
            return result.scalars().all()
        else:
            await session.execute(stmt, data)

    # MARK: Count
    @classmethod
    async def count(
        cls,
        *where,
        session: AsyncSession,
    ) -> int:
        """
        Посчитать строки в БД, соответствующий критериям.

        Returns:
            rows_count: количество найденных строк или 0 если совпадений не найдено.
        """

        stmt = select(func.count()).select_from(cls.model).where(*where)
        return await session.scalar(stmt) or 0

    # MARK: Find
    @classmethod
    async def find_all_sorted(
        cls,
        *where,
        session: AsyncSession,
        order_by,
        offset: int | None,
        limit: int | None,
        asc: bool,
    ) -> list[ModelType]:
        """
        Получить все записи с фильтрацией по переданным
        query-параметрам и с учетом пагинации.
        """

        stmt = (
            select(cls.model)
            .where(*where)
            .offset(offset)
            .limit(limit)
            .order_by(order_by.asc() if asc else order_by.desc())
        )
        result = await session.execute(stmt)
        return result.scalars().all()
