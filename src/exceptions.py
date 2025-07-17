from fastapi import HTTPException, status


class HeroNotFound(HTTPException):
    """Возникает, если герой не найден."""

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Герой не найден",
        )


class HeroAlreadyExists(HTTPException):
    """Возникает, если герой с переданным именем уже существует в БД."""

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail="Герой с переданным именем уже существует в БД",
        )


class SuperHeroAPINotAvailable(HTTPException):
    """Возникает, если сервис SuperHeroAPI не доступен."""

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Сервис SuperHeroAPI не доступен.",
        )
