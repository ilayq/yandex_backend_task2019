from sqlalchemy import select, and_
from db.models.models import CitizenORM, CitizenList, RelativeORM
from db.util import engine
from typing import Optional
from db.util import citizen_fields


async def imports_get_by_id(import_id: int) -> Optional[CitizenList]:
    cits = []
    rows = get_citizens_rows(import_id)
    if not rows:
        return None
    async for r in rows:
        cits.append({})
        for value, key in zip(r, citizen_fields):
            cits[-1][key] = value

        del cits[-1]['import_id']
        cits[-1]['birth_date'] = '.'.join(str(cits[-1]['birth_date']).split('-')[::-1])
        cits[-1]['relatives'] = [citizen_id async for citizen_id in get_citizens_relatives(import_id, cits[-1]['citizen_id'])]

    return CitizenList(citizens=cits)


async def get_citizens_rows(import_id: int):
    q = select(CitizenORM).where(CitizenORM.import_id == import_id)
    with engine.connect() as db:
        for row in db.execute(q):
            yield row


async def get_citizens_relatives(import_id: int, citizen_id: int):
    q = select(RelativeORM.relative_id).where(and_(RelativeORM.citizen_id == citizen_id, RelativeORM.import_id == import_id))
    with engine.connect() as db:
        for row in db.execute(q):
            yield row[0]


if __name__ == '__main__':
    import asyncio
    print(asyncio.run(imports_get_by_id(1)))
