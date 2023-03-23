import json
from asyncio import run
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from settings import DB_CONNECTION_STRING
from db.models.models import CitizenORM, Relative, Import


async def imports_post_handler(json_file=None) -> dict:
    # with open('json.json', encoding='utf-8') as jsonstring:
    #     data = json.load(jsonstring)
    engine = create_engine(DB_CONNECTION_STRING + '/yandex_backend_task')
    session = sessionmaker(autoflush=False, bind=engine)
    relations = dict()
    # insert import_id in imports and remember it
    with session(autoflush=False, bind=engine) as db:
        imp = Import()
        db.add(imp)
        db.commit()
        db.refresh(imp)
        main_import_id = imp.import_id
        db.close()
    # iter citizens, add to db and save relations between them
    with session(autoflush=False, bind=engine) as db:
        for citizen in data['citizens']:
            citizen_id = citizen['citizen_id']
            relations[citizen_id] = citizen['relatives']
            town = citizen['town']
            street = citizen['street']
            building = citizen['building']
            apartment = citizen['apartment']
            name = citizen['name']
            birth_date = '.'.join(citizen['birth_date'].split('.')[::-1])
            gender = citizen['gender']
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
        for citizen in relations:
            if not relations[citizen]:
                continue
            for relative in relations[citizen]:
                rel = Relative(citizen_id=citizen,
                               import_id=main_import_id,
                               relative_id=relative)
                db.add(rel)
            db.commit()
        db.close()
    return {"data": {"import_id": main_import_id}}

#TODO CHECK IF IMPORT IS VALID

if __name__ == '__main__':
    run(imports_post_handler())
