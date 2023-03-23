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


def sqlaclhemy_init():
    with create_engine(DB_CONNECTION_STRING + '/postgres',
                       isolation_level='AUTOCOMMIT').connect() as con:
        t = text('CREATE DATABASE yandex_backend_task')
        con.execute(t)
        con.commit()
    from enum import Enum, unique

    from sqlalchemy import (
        Column, Date, Enum as PgEnum, ForeignKey, ForeignKeyConstraint, Integer,
        MetaData, String, Table,
    )

    # SQLAlchemy рекомендует использовать единый формат для генерации названий для
    # индексов и внешних ключей.
    # https://docs.sqlalchemy.org/en/13/core/constraints.html#configuring-constraint-naming-conventions
    convention = {
        'all_column_names': lambda constraint, table: '_'.join([
            column.name for column in constraint.columns.values()
        ]),
        'ix': 'ix__%(table_name)s__%(all_column_names)s',
        'uq': 'uq__%(table_name)s__%(all_column_names)s',
        'ck': 'ck__%(table_name)s__%(constraint_name)s',
        'fk': 'fk__%(table_name)s__%(all_column_names)s__%(referred_table_name)s',
        'pk': 'pk__%(table_name)s'
    }

    metadata = MetaData(naming_convention=convention)

    @unique
    class Gender(Enum):
        female = 'female'
        male = 'male'

    imports_table = Table(
        'imports',
        metadata,
        Column('import_id', Integer, primary_key=True)
    )

    citizens_table = Table(
        'citizens',
        metadata,
        Column('import_id', Integer, ForeignKey('imports.import_id'),
               primary_key=True),
        Column('citizen_id', Integer, primary_key=True),
        Column('town', String, nullable=False, index=True),
        Column('street', String, nullable=False),
        Column('building', String, nullable=False),
        Column('apartment', Integer, nullable=False),
        Column('name', String, nullable=False),
        Column('birth_date', Date, nullable=False),
        Column('gender', PgEnum(Gender, name='gender'), nullable=False),
    )

    relations_table = Table(
        'relations',
        metadata,
        Column('import_id', Integer, primary_key=True),
        Column('citizen_id', Integer, primary_key=True),
        Column('relative_id', Integer, primary_key=True),
        ForeignKeyConstraint(
            ('import_id', 'citizen_id'),
            ('citizens.import_id', 'citizens.citizen_id')
        ),
        ForeignKeyConstraint(
            ('import_id', 'relative_id'),
            ('citizens.import_id', 'citizens.citizen_id')
        ),
    )