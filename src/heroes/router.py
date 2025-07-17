from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.dependencies import get_session
from src.heroes.schemas import HeroListReadSchema, HeroQuerySchema
from src.heroes.service import HeroesService

__all__ = ["heroes_router"]

heroes_router = APIRouter(prefix="/heroes", tags=["Супер-герои"])


# MARK: Get
@heroes_router.get(
    "",
    summary="Получить список героев",
    status_code=status.HTTP_200_OK,
    response_model=None,
    responses={status.HTTP_200_OK: {"model": HeroListReadSchema}},
)
async def get_heroes_route(
    query: HeroQuerySchema = Query(),
    session: AsyncSession = Depends(get_session),
) -> HeroListReadSchema:
    """
    Получить список героев с фильтрацией по переданным
    query-параметрам и с учетом пагинации.

    По умолчанию сортировка выполняется по id героя.

    Raises:

        HeroNotFound: Герой не найден `HTTP_404_NOT_FOUND`.
    """

    return await HeroesService.get_heroes(query=query, session=session)


# MARK: Post
@heroes_router.post(
    "",
    summary="Создать нового героя",
    status_code=status.HTTP_201_CREATED,
    response_model=None,
    responses={status.HTTP_201_CREATED: {"model": HeroListReadSchema}},
)
async def create_hero_route(
    name: str = Query(description="Имя героя"),
    session: AsyncSession = Depends(get_session),
) -> HeroListReadSchema:
    """
    Создать нового героя.

    Выполняется поиск героя по имени в сервисе [SuperHero API](https://superheroapi.com/).
    Если найдены несколько героев, все будут добавлены в БД.

    Возвращаются данные созданных героев.

    Raises:

        SuperHeroAPINotAvailable: Сервис SuperHeroAPI не доступен `HTTP_503_SERVICE_UNAVAILABLE`.
        HeroNotFound: Герой не найден `HTTP_404_NOT_FOUND`.
        HeroAlreadyExists: Герой с переданным именем уже существует в БД `HTTP_409_CONFLICT`.
    """

    return await HeroesService.create_hero(name=name, session=session)
