import fastapi
import uvicorn
import handlers
from db.models.models import CitizenList, CitizenPatch


app = fastapi.FastAPI()


@app.post('/imports')
async def imports_post(citizens: CitizenList):
    handler_response = await handlers.imports_post_handler(citizens)
    if handler_response:
        return {"data": handler_response}
    raise fastapi.HTTPException(status_code=404, detail="invalid json")


@app.patch('/imports/{import_id}/citizens/{citizen_id}')
async def imports_patch(import_id: int, citizen_id: int, new_params: CitizenPatch):
    handler_response = await handlers.patch_citizen_handler(parameters=new_params.dict(),
                                                            import_id=import_id,
                                                            citizen_id=citizen_id)
    if handler_response:
        return handler_response
    raise fastapi.HTTPException(status_code=404, detail="invalid json"
                                                        " / citizen_id not found /"
                                                        " import_id not found")


@app.get('/imports/{import_id}/citizens')
async def imports_get_citizens(import_id: int):
    result = await handlers.imports_get_by_id(import_id)
    if not result:
        raise fastapi.HTTPException(status_code=404, detail="import_id_not_found")
    return result


@app.get('/imports/{import_id}/citizens/birthdays')
async def import_get_birthdays(import_id: int):
    result = await handlers.birthdays_handler(import_id=import_id)
    if not result:
        raise fastapi.HTTPException(status_code=404, detail="import_id not found")
    return result


@app.get('/imports/{import_id}/towns/stat/percentile/age')
async def import_get_stats_by_age(import_id: int):
    result = await handlers.import_get_stats_by_age(import_id)
    if not result:
        raise fastapi.HTTPException(status_code=404, detail="import_id not found")
    return result


if __name__ == '__main__':
    uvicorn.run('app:app', reload=True)
