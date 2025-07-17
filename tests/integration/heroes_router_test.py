import copy

import httpx
from fastapi import status
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.heroes.dao import HeroDAO
from src.heroes.models import HeroModel
from src.heroes.router import heroes_router
from src.heroes.schemas import HeroListReadSchema, HeroQuerySchema
from tests.integration.conftest import BaseTestRouter


class TestHeroesRouter(BaseTestRouter):
    """
    Класс для тестирования эндпоинтов роутера `heroes_router`.

    Герои загружаются в БД предварительно при запуске тестов
    из фикстуры `alembic/fixtures/heroes.json`.
    """

    router = heroes_router

    # MARK: Get
    async def test_get_heroes_no_query(
        self, session: AsyncSession, router_client: httpx.AsyncClient
    ):
        """Возможно получить героев из БД без использования query параметров."""

        heroes_count = await HeroDAO.count(session=session)

        response = await router_client.get(url="/heroes")
        assert response.status_code == status.HTTP_200_OK

        heroes_data = HeroListReadSchema(**response.json())
        assert heroes_data.count == heroes_count

    async def test_get_heroes_query(
        self, session: AsyncSession, router_client: httpx.AsyncClient
    ):
        """Возможно получить героев из БД c использованием query параметров."""

        batmans_count = await HeroDAO.count(HeroModel.name == "Batman", session=session)

        # Героев с именем `Batman` в БД два
        response = await router_client.get(
            url="/heroes",
            params=HeroQuerySchema(name="Batman").model_dump(exclude_unset=True),
        )
        assert response.status_code == status.HTTP_200_OK

        heroes_data = HeroListReadSchema(**response.json())
        assert heroes_data.count == batmans_count

        assert heroes_data.heroes[0].name == "Batman"
        assert heroes_data.heroes[1].name == "Batman"

        # Т.к. сортировка по умолчанию выполняются по возрастанию `id`,
        # проверяем соответствие id героев в ответе id героев в фикстуре
        assert heroes_data.heroes[0].id == 69
        assert heroes_data.heroes[1].id == 70

    # MARK: Post
    async def test_create_hero(
        self, session: AsyncSession, router_client: httpx.AsyncClient, mocker
    ):
        """Возможно добавить героя в БД."""

        # Удаляем первого героя в фикстуре и получаем его данные для последующего добавления
        stmt = delete(HeroModel).where(HeroModel.id == 69).returning(HeroModel)
        hero_db = await session.scalar(stmt)
        hero_data = copy.copy(hero_db.__dict__)

        # Мок получения данных героя в сервисе SuperHeroAPI
        mocker.patch(
            "src.heroes.service.HeroesService._fetch_from_superhero_api",
            return_value=[hero_data],
        )

        response = await router_client.post(url="/heroes", params={"name": "Batman"})
        assert response.status_code == status.HTTP_201_CREATED

        heroes_data = HeroListReadSchema(**response.json())
        assert heroes_data.count == 1

        assert heroes_data.heroes[0].name == "Batman"
        assert heroes_data.heroes[0].id == 69
