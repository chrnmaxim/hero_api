import aiohttp
from fastapi import status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src import exceptions
from src.config import api_settings
from src.heroes.dao import HeroDAO
from src.heroes.models import HeroModel
from src.heroes.schemas import HeroListReadSchema, HeroQuerySchema


class HeroesService:
    """
    Класс для работы с героями.

    Позволяет выполнять CRUD операции.
    """

    # MARK: Utils
    @classmethod
    async def _fetch_from_superhero_api(cls, name: str) -> list[dict]:
        """
        Получить данные героя по его имени в сервисе
        [SuperHero API](https://superheroapi.com/).

        Raises:
            SuperHeroAPINotAvailable: Сервис SuperHeroAPI не доступен `HTTP_503_SERVICE_UNAVAILABLE`.
            HeroNotFound: Герой не найден `HTTP_404_NOT_FOUND`.
        """

        async with aiohttp.ClientSession() as session:
            async with session.get(
                url=f"https://superheroapi.com/api/{api_settings.SUPERHERO_API_TOKEN}/search/{name}"
            ) as response:
                if response.status != status.HTTP_200_OK:
                    raise exceptions.SuperHeroAPINotAvailable
                heroes_data = await response.json()
                if (
                    heroes_data.get("error", "")
                    == "character with given name not found"
                ):
                    raise exceptions.HeroNotFound
                return heroes_data["results"]

    # MARK: Create
    @classmethod
    async def create_hero(cls, name: str, session: AsyncSession) -> HeroListReadSchema:
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

        heroes_data = await cls._fetch_from_superhero_api(name=name)
        for hero_data in heroes_data:
            hero_data["id"] = int(hero_data["id"])

        try:
            await HeroDAO.add_bulk(session=session, data=heroes_data)
        except IntegrityError as ex:
            raise exceptions.HeroAlreadyExists from ex

        await session.commit()

        return HeroListReadSchema(count=len(heroes_data), heroes=heroes_data)

    # MARK: Read
    @classmethod
    async def get_heroes(
        cls, query: HeroQuerySchema, session: AsyncSession
    ) -> HeroListReadSchema:
        """
        Получить список героев с фильтрацией по переданным
        query-параметрам и с учетом пагинации.

        Raises:
            HeroNotFound: Герой не найден `HTTP_404_NOT_FOUND`.
        """

        filters = HeroDAO.prepare_filters_by_query(query=query)
        count = await HeroDAO.count(*filters, session=session)
        if count:
            heroes = await HeroDAO.find_all_sorted(
                *filters,
                session=session,
                order_by=HeroModel.id,
                offset=query.offset,
                limit=query.limit,
                asc=query.asc,
            )
            return HeroListReadSchema(count=count, heroes=heroes)
        else:
            raise exceptions.HeroNotFound
