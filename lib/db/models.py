from sqlalchemy import ForeignKey, Column, Integer, String, MetaData
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)

class Answer(Base):
    __tablename__='answers'

    id=Column(Integer(),primary_key=True)
    category=Column(String())
    answer=Column(String())

class Question(Base):
    __tablename__='questions'

    id=Column(Integer(), primary_key=True)
    question=Column(String())
    difficulty=Column(Integer())
    category=Column(String())

    answer_id=Column(Integer(), ForeignKey('answers.id'))



