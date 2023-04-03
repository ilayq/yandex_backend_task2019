from sqlalchemy import select, and_
from db.models.models import CitizenORM
from db.util import engine
import numpy as np
import datetime


async def import_get_stats_by_age(import_id: int) -> list[dict]:
    q = select(CitizenORM.town).where(CitizenORM.import_id == import_id).distinct()
    with engine.connect() as db:
        cities = db.execute(q).fetchall()
    result = []
    for town in cities:
        result.append({})
        result[-1]['town'] = town[0]
        town_ages = [bd async for bd in get_ages_by_cities(import_id, town[0])]
        town_ages = np.array(town_ages)
        result[-1]['p50'] = np.percentile(town_ages, 50)
        result[-1]['p75'] = np.percentile(town_ages, 75)
        result[-1]['p99'] = np.percentile(town_ages, 99)
    return result


async def get_ages_by_cities(import_id, city: str):
    q = select(CitizenORM.birth_date).where(and_(CitizenORM.import_id == import_id, CitizenORM.town == city))
    with engine.connect() as db:
        result = db.execute(q).fetchall()

    for bd in result:
        yield ((datetime.date.today() - bd[0]) // 365).days


if __name__ == '__main__':
    import asyncio
    asyncio.run(import_get_stats_by_age(1))
