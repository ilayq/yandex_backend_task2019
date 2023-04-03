from sqlalchemy import create_engine
from settings import DB_CONNECTION_STRING
from sqlalchemy import text


with create_engine(DB_CONNECTION_STRING + '/postgres',
                   isolation_level='AUTOCOMMIT').connect() as con:
    t = text('CREATE DATABASE yandex_backend_task')
    con.execute(t)
with create_engine(DB_CONNECTION_STRING + '/yandex_backend_task',
                   isolation_level='AUTOCOMMIT').connect() as con:
    t = text('CREATE TABLE imports(import_id SERIAL PRIMARY KEY)')
    con.execute(t)
    t = text('CREATE TABLE citizens('
             'citizen_id INTEGER,'
             'import_id INTEGER,'
             'town varchar(256) NOT NULL,'
             'street varchar(256) NOT NULL,'
             'building varchar(256) NOT NULL,'
             'apartment INTEGER CHECK (apartment > 0) NOT NULL,'
             'name varchar(256) NOT NULL,'
             'birth_date DATE NOT NULL,'
             'gender varchar(7),'
             'FOREIGN KEY (import_id) REFERENCES imports (import_id) ON DELETE CASCADE,'
             'PRIMARY KEY (citizen_id, import_id))')
    con.commit()
    con.execute(t)
    con.commit()
    t = text('CREATE TABLE relations('
             'import_id INTEGER,'
             'citizen_id INTEGER,'
             'relative_id INTEGER,'
             'FOREIGN KEY (import_id, citizen_id) REFERENCES citizens (import_id, citizen_id) ON DELETE CASCADE,'
             'FOREIGN KEY (import_id, relative_id) REFERENCES citizens (import_id, citizen_id) ON DELETE CASCADE)')
    con.execute(t)
    con.commit()
