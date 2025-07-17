# HeroesAPI

[![Static Badge](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://www.python.org)
[![Static Badge](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Static Badge](https://img.shields.io/badge/-Swagger-%23Clojure?style=for-the-badge&logo=swagger&logoColor=white)](https://swagger.io)
[![Static Badge](https://img.shields.io/badge/postgresql-4169e1?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org)
[![Static Badge](https://img.shields.io/badge/-SQLAlchemy-ffd54?style=for-the-badge&logo=sqlalchemy&logoColor=white)](https://www.sqlalchemy.org/)
[![Static Badge](https://img.shields.io/badge/docker-257bd6?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)

Проект позволяет добавлять супер-героев, найденных в сервисе [SuperHeroAPI](https://superheroapi.com/index.html), в локальную БД.
Также можно получать героев, которые уже были добавлены в БД.

## Установка проекта

1. Установить [uv](https://docs.astral.sh/uv/getting-started/installation/).

2. Клонировать проект:

```bash
git clone git@github.com:chrnmaxim/hero_api.git
```

3. Перейти в корневую директорию проекта.

4. Установить зависимости, включая зависимости для разработки:
```bash
uv sync --extra dev
```

5. Создать `.env` на основании `.env.example`:

```bash
cp -r src/.env.example src/.env`
```

> [!NOTE]
> Необходимо указать ваш токен для SuperHeroAPI, который можно получить [здесь](https://superheroapi.com/#intro), выполнив вход через GitHub.

6. Запустить API вместе PostgreSQL в Docker контейнерах и применить миграции БД:
```bash
make start_dev
```

7. Документация API и доступные эндпоинт:
* Swagger UI: http://127.0.0.1:8000/docs
* ReDoc: http://127.0.0.1:8000/redoc

8. Для удаления контейнеров выполнить
```bash
make remove_dev
```

## Тесты
1. Тесты запускаются из независимой базы данных PostgreSQL с помощью команды `make test`.

2. После выполнения тестов в файле `htmlcov/index.html` можно увидеть отчет о покрытии кода тестами.

> [!NOTE]
> Тесты запускаются в GitHub Actions с каждым коммитом в открытом Pull Request в ветку `develop`.
