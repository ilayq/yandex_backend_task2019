import fastapi
import uvicorn
from handlers.imports_post import imports_post_handler


app = fastapi.FastAPI()


@app.post('/imports')
async def imports_post(json_file):
    ...
    return await imports_post_handler(json_file)


@app.patch('/imports/{import_id}/citizens/{citizen_id}')
async def imports_patch(import_id: int, citizen_id: int):
    ...


@app.get('/imports/{import_id}/citizens')
async def imports_get_citizens(import_id: int):
    ...


@app.get('/imports/{import_id}/citizens/birthdays')
async def import_get_birthdays(import_id: int):
    ...


@app.get('/imports/{import_id}/towns/stat/percentile/age')
async def import_get_stats_by_age(import_id: int):
    ...


if __name__ == '__main__':
    uvicorn.run('app:app', reload=True)
