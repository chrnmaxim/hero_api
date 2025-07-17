from sqlalchemy import Integer, and_, cast

from src.dao import BaseDAO
from src.heroes.models import HeroModel
from src.heroes.schemas import HeroQuerySchema, HeroReadSchema


class HeroDAO(BaseDAO[HeroModel, HeroReadSchema]):
    """DAO для работы с героями."""

    model = HeroModel

    @classmethod
    def prepare_filters_by_query(cls, query: HeroQuerySchema) -> list:
        """Подготовить список фильтров для запроса списка героев в БД."""

        filters = []
        stat_fields = [
            "intelligence",
            "strength",
            "speed",
            "durability",
            "power",
            "combat",
        ]
        query_data = query.model_dump(exclude_none=True, exclude_unset=True)

        for field in stat_fields:
            value = query_data.get(field, None)
            min_value = query_data.get(f"{field}_min", None)
            max_value = query_data.get(f"{field}_max", None)

            json_field = HeroModel.powerstats[field].astext

            if value is not None:
                filters.append(
                    and_(json_field != "null", cast(json_field, Integer) == value)
                )
            else:
                if min_value is not None:
                    filters.append(
                        and_(
                            json_field != "null", cast(json_field, Integer) >= min_value
                        )
                    )
                if max_value is not None:
                    filters.append(
                        and_(
                            json_field != "null", cast(json_field, Integer) <= max_value
                        )
                    )

        if query.name is not None:
            filters.append(HeroModel.name == query.name)

        return filters
