import datetime
from datetime import date
from sqlalchemy import Column, Integer, Date, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel, ValidationError, validator
from typing import List, Optional


Base = declarative_base()


class ImportORM(Base):
    __tablename__ = 'imports'

    import_id = Column(Integer, primary_key=True, autoincrement=True)


class CitizenORM(Base):
    __tablename__ = 'citizens'

    citizen_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    import_id = Column(Integer, ForeignKey("imports.import_id"))
    town = Column(String(256), nullable=False)
    street = Column(String(256), nullable=False)
    building = Column(String(256), nullable=False)
    apartment = Column(Integer, nullable=False)
    name = Column(String(256), nullable=False)
    birth_date = Column(Date, nullable=False)
    gender = Column(String(256), nullable=False)


class Citizen(BaseModel):
    citizen_id: int
    town: str
    street: str
    building: str
    apartment: int
    name: str
    birth_date: str
    gender: str
    relatives: Optional[List[int]] = []

    def from_orm(obj: CitizenORM):
        d = obj.__dict__
        cit = Citizen(
            citizen_id=d['citizen_id'],
            town=d['town'],
            street=d['street'],
            building=d['building'],
            apartment=d['apartment'],
            name=d['name'],
            birth_date=d['birth_date'].strftime("%d.%m.%Y"),
            gender=d['gender'],
            relatives=[],
        )
        return cit

    @validator('citizen_id')
    def validate_citizen_id(cls, v: int):
        assert type(v) == int
        assert v > 0
        return v

    @validator('town')
    def validate_town(cls, v: str):
        assert len(v) <= 256
        assert v.strip() != ''
        return v

    @validator('street')
    def validate_street(cls, v: str):
        assert len(v) <= 256
        assert v.strip() != ''
        return v

    @validator('building')
    def validate_building(cls, v: str):
        assert len(v) <= 256
        assert v.strip() != ''
        return v

    @validator('apartment')
    def validate_apartment(cls, v: int):
        assert type(v) == int
        assert v > 0
        return v

    @validator('name')
    def validate_name(cls, v: str):
        assert len(v) <= 256
        assert v.strip() != ''
        return v

    @validator('birth_date')
    def validate_bd(cls, v: str):
        try:
            bd = date.fromisoformat('-'.join(v.split('.')[::-1]))
            assert bd < datetime.date.today()
        except Exception:
            raise ValidationError
        return v

    @validator('gender')
    def validate_gender(cls, v: str):
        assert v.strip() == 'male' or v == 'female'
        return v

    class Config:
        orm_mode = True
        validate_assignment = True


class CitizenList(BaseModel):
    citizens: List[Citizen]

    class Config:
        validate_assingment = True

class CitizenPatch(BaseModel):
    town: Optional[str]
    street: Optional[str]
    building: Optional[str]
    apartment: Optional[int]
    name: Optional[str]
    birth_date: Optional[str]
    gender: Optional[str]
    relatives: Optional[List[int]] = []


class PresentsResponse(BaseModel):
    citizen_id: int
    presents: int


class RelativeORM(Base):
    __tablename__ = 'relations'

    import_id = Column(Integer, ForeignKey("imports.import_id"))
    citizen_id = Column(Integer, ForeignKey('citizens.citizen_id'), primary_key=True,)
    relative_id = Column(Integer, ForeignKey('citizens.citizen_id'))


if __name__ == '__main__':
    c = Citizen(citizen_id='-1',
                import_id=2,
                town=1,
                street='2',
                building='2',
                apartment=23,
                name='asd',
                birth_date='123',
                gender='male')
    print(c)
