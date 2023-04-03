"""
1. iter months
2. find citizens with current month
3. add his relatives to result or increment their value
4. return dict[month: list[citizen_id: presents]]
"""

from sqlalchemy import select, and_
from db.models.models import ImportORM, CitizenORM, RelativeORM, PresentsResponse
from db.util import session, engine
from typing import Optional


async def validate_import_id(import_id: int) -> bool:
    """check if import_id exist in db"""
    query = select(ImportORM).where(ImportORM.import_id == import_id)
    with session(bind=engine) as db:
        result = db.execute(query).first()
    if not result:
        return False
    return True


async def birthdays_handler(import_id: int) -> Optional[dict]:
    check = await validate_import_id(import_id)
    if not check:
        return None
    response = dict()
    for month in range(1, 13):
        response[month] = []
    relations = dict()
    # find citizens and their relatives
    query = select(RelativeORM.citizen_id, RelativeORM.relative_id).where(RelativeORM.import_id == import_id)
    with session(bind=engine) as db:
        result = db.execute(query).fetchall()
    for row in result:
        if row[0] == row[1]:
            continue
        if row[0] not in relations:
            relations[row[0]] = []
        relations[row[0]].append(row[1])
    for citizen in relations:
        for relative in relations[citizen]:
            # get birth_date of relative
            query = select(CitizenORM.birth_date).where(and_(CitizenORM.import_id == import_id,
                                                             CitizenORM.citizen_id == relative))
            with session(bind=engine) as db:
                bd_month = db.execute(query).first()[0].month
            flag = True
            for cit in response[bd_month]:
                if cit.citizen_id == citizen:
                    cit.presents += 1
                    flag = False
                    break
            if flag:
                response[bd_month].append(PresentsResponse(citizen_id=citizen,
                                                           presents=1))
    return response


if __name__ == '__main__':
    import asyncio

    asyncio.run(birthdays_handler(1))
