from db.util import session, engine
from db.models.models import CitizenORM, Citizen, RelativeORM
from sqlalchemy import select, update, and_, delete
from typing import Optional


async def validate_request(parameters: dict, import_id: int, citizen_id: int) -> bool:
    print(parameters)
    if not len(parameters):
        return False

    if 'citizen_id' in parameters:
        return False

    params_for_delete = []
    for param in parameters:
        if parameters[param] is None:
            params_for_delete.append(param)
    for param in params_for_delete:
        del parameters[param]

    # check if citizen exists
    query = select(CitizenORM).where(and_(CitizenORM.citizen_id == citizen_id,
                                          CitizenORM.import_id == import_id))
    with session(bind=engine) as s:
        res = s.scalars(query).first()

    if not res:
        return False

    # validating new fields except relations
    existing_user = res
    existing_user_dict = Citizen.from_orm(existing_user).dict()
    try:
        for param in parameters:
            existing_user_dict[param] = parameters[param]
        Citizen.parse_obj(existing_user_dict)
    except Exception:
        return False

    # validate relations
    if 'relatives' in parameters:
        q = select(CitizenORM.citizen_id).where(CitizenORM.import_id == import_id)
        with engine.connect() as s:
            rows = s.execute(q).fetchall()

        all_citizens = set()
        for cit in rows:
            all_citizens.add(cit[0])

        if set(parameters['relatives']) - all_citizens:
            return False

    return True


async def patch_citizen_handler(parameters: dict, import_id: int, citizen_id: int) -> Optional[Citizen]:
    check = await validate_request(parameters, import_id, citizen_id)

    if not check:
        return None

    if 'relatives' not in parameters:
        q = update(CitizenORM).where(and_(CitizenORM.citizen_id == citizen_id,
                                          CitizenORM.import_id == import_id)).values(parameters)
        with engine.connect() as db:
            db.execute(q)
            db.commit()
            db.close()
        query = select(CitizenORM).where(CitizenORM.citizen_id == citizen_id and
                                         CitizenORM.import_id == import_id)
        with session(bind=engine) as db:
            updated_citizen = db.scalars(query).first()
        updated_citizen = Citizen.from_orm(updated_citizen)
        query = select(RelativeORM.relative_id).where(and_(RelativeORM.citizen_id == citizen_id,
                                                           RelativeORM.import_id == import_id))
        with session(bind=engine) as db:
            relatives = db.execute(query).fetchall()
        for relative in relatives:
            updated_citizen.relatives.append(relative[0])
    else:
        new_relatives = set(parameters['relatives'].copy())
        del parameters['relatives']
        if parameters:
            q = update(CitizenORM).where(and_(CitizenORM.citizen_id == citizen_id,
                                              CitizenORM.import_id == import_id)).values(parameters)
            with session(bind=engine) as db:
                db.execute(q)
                db.commit()
                db.close()
        query = select(RelativeORM.relative_id).where(and_(RelativeORM.citizen_id == citizen_id,
                                                           RelativeORM.import_id == import_id))
        with session(bind=engine) as db:
            old_relatives = db.execute(query).fetchall()
        for i in range(len(old_relatives)):
            old_relatives[i] = old_relatives[i][0]
        old_relatives = set(old_relatives)

        for relative in old_relatives - new_relatives:
            query = delete(RelativeORM).where(and_(RelativeORM.relative_id == relative,
                                                   RelativeORM.citizen_id == citizen_id,
                                                   RelativeORM.import_id == import_id))
            with session(bind=engine) as db:
                db.execute(query)
                db.commit()
                db.close()

            query = delete(RelativeORM).where(and_(RelativeORM.citizen_id == relative,
                                                   RelativeORM.relative_id == citizen_id,
                                                   RelativeORM.import_id == import_id))
            with session(bind=engine) as db:
                db.execute(query)
                db.commit()
                db.close()

        for relative in new_relatives - old_relatives:
            with session(bind=engine) as db:
                db.add(RelativeORM(import_id=import_id,
                                   citizen_id=citizen_id,
                                   relative_id=relative))
                db.add(RelativeORM(import_id=import_id,
                                   citizen_id=relative,
                                   relative_id=citizen_id))
                db.commit()
                db.close()

        query = select(CitizenORM).where(CitizenORM.citizen_id == citizen_id and
                                         CitizenORM.import_id == import_id)
        with session(bind=engine) as db:
            updated_citizen = db.scalars(query).first()
        updated_citizen = Citizen.from_orm(updated_citizen)
        updated_citizen.relatives = list(new_relatives)
        print(updated_citizen)
    return updated_citizen


if __name__ == '__main__':
    import asyncio

    asyncio.run(patch_citizen_handler({'relatives': [2]}, 1, 1))
