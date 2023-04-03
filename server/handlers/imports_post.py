from asyncio import run
from db.models.models import Citizen, CitizenORM, RelativeORM, ImportORM, CitizenList
from db.util import session, engine
from typing import List


async def imports_post_handler(citizens: CitizenList) -> int:
    citizens = citizens.citizens
    check = await check_import_is_valid(citizens)

    if not check:
        return 0

    # insert import_id in imports and remember it
    with session(autoflush=False, bind=engine) as db:
        imp = ImportORM()
        db.add(imp)
        db.commit()
        db.refresh(imp)
        main_import_id = imp.import_id
        db.close()

    relations = dict()

    # iter citizens, add to db and save relations between them
    with session(autoflush=False, bind=engine) as db:
        for citizen in citizens:
            citizen_id = citizen.citizen_id
            relations[citizen.citizen_id] = citizen.relatives
            town = citizen.town
            street = citizen.street
            building = citizen.building
            apartment = citizen.apartment
            name = citizen.name
            birth_date = '.'.join(citizen.birth_date.split('.')[::-1])
            gender = citizen.gender
            cur_citizen = CitizenORM(citizen_id=citizen_id,
                                     import_id=main_import_id,
                                     town=town,
                                     street=street,
                                     building=building,
                                     apartment=apartment,
                                     name=name,
                                     birth_date=birth_date,
                                     gender=gender)
            db.add(cur_citizen)
            db.commit()

    # iter relations and insert into relations
    with session(autoflush=False, bind=engine) as db:
        for citizen_id in relations:
            if not relations[citizen_id]:
                continue
            for relative_id in relations[citizen_id]:
                rel = RelativeORM(citizen_id=citizen_id,
                                  import_id=main_import_id,
                                  relative_id=relative_id)
                db.add(rel)
            db.commit()
        db.close()
    return main_import_id


async def check_import_is_valid(citizens: List[Citizen]) -> bool:
    relations = dict()
    # checking field except relations
    for citizen in citizens:
        relations[citizen.citizen_id] = citizen.relatives

    # checking relations
    for citizen in relations:
        for relative in relations[citizen]:
            if citizen not in relations[relative]:
                return False

    return True

