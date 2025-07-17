from pydantic import BaseModel, ConfigDict, Field, HttpUrl

from src.base_schemas import BaseListReadSchema, BaseQuerySchema


# MARK: Query
class HeroQuerySchema(BaseQuerySchema):
    """Схема query-параметров для поиска героев."""

    name: str | None = None

    intelligence: int | None = None
    intelligence_min: int | None = None
    intelligence_max: int | None = None

    strength: int | None = None
    strength_min: int | None = None
    strength_max: int | None = None

    speed: int | None = None
    speed_min: int | None = None
    speed_max: int | None = None

    durability: int | None = None
    durability_min: int | None = None
    durability_max: int | None = None

    power: int | None = None
    power_min: int | None = None
    power_max: int | None = None

    combat: int | None = None
    combat_min: int | None = None
    combat_max: int | None = None


# MARK: Heroes
class HeroPowerStatsSchema(BaseModel):
    """Схема характеристик героя."""

    intelligence: str
    strength: str
    speed: str
    durability: str
    power: str
    combat: str


class HeroBiographySchema(BaseModel):
    """Схема биографии героя."""

    full_name: str = Field(alias="full-name")
    alter_egos: str = Field(alias="alter-egos")
    aliases: list[str]
    place_of_birth: str = Field(alias="place-of-birth")
    first_appearance: str = Field(alias="first-appearance")
    publisher: str
    alignment: str

    model_config = ConfigDict(validate_by_alias=True, serialize_by_alias=True)


class HeroAppearanceSchema(BaseModel):
    """Схема описания внешности героя."""

    gender: str
    race: str
    height: list[str]
    weight: list[str]
    eye_color: str = Field(alias="eye-color")
    hair_color: str = Field(alias="hair-color")

    model_config = ConfigDict(validate_by_alias=True, serialize_by_alias=True)


class HeroWorkSchema(BaseModel):
    """Схема данных о работе героя."""

    occupation: str
    base: str


class HeroConnectionsSchema(BaseModel):
    """Схема данных о связях героя."""

    group_affiliation: str = Field(alias="group-affiliation")
    relatives: str

    model_config = ConfigDict(validate_by_alias=True, serialize_by_alias=True)


class HeroImageSchema(BaseModel):
    """Схема изображения героя."""

    url: HttpUrl


class HeroReadSchema(BaseModel):
    """Схема для отображения полных данных героя."""

    id: int
    name: str
    powerstats: HeroPowerStatsSchema
    biography: HeroBiographySchema
    appearance: HeroAppearanceSchema
    work: HeroWorkSchema
    connections: HeroConnectionsSchema
    image: HeroImageSchema

    model_config = ConfigDict(from_attributes=True)


class HeroListReadSchema(BaseListReadSchema):
    """Схема для отображения героев в списке."""

    heroes: list[HeroReadSchema]
