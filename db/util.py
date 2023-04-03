from settings import DB_CONNECTION_STRING
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


engine = create_engine(DB_CONNECTION_STRING + '/yandex_backend_task')
session = sessionmaker(autoflush=False, bind=engine)


citizen_fields = [
    "citizen_id",
    "import_id",
    "town",
    "street",
    "building",
    "apartment",
    "name",
    "birth_date",
    "gender"
]