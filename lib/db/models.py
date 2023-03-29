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


class Player(Base):
    __tablename__='players'

    id=Column(Integer(), primary_key=True)
    username=Column(String())
    password=Column(String())

class Game(Base):
    __tablename__='games'

    id=Column(Integer(), primary_key=True)
    score=Column(Integer())
    
    player_id=Column(Integer(), ForeignKey('players.id'))
    question_1_id=Column(Integer(), ForeignKey('questions.id'))
    question_2_id=Column(Integer(), ForeignKey('questions.id'))
    question_3_id=Column(Integer(), ForeignKey('questions.id'))
    question_4_id=Column(Integer(), ForeignKey('questions.id'))
    question_5_id=Column(Integer(), ForeignKey('questions.id'))
    question_6_id=Column(Integer(), ForeignKey('questions.id'))
    question_7_id=Column(Integer(), ForeignKey('questions.id'))
    question_8_id=Column(Integer(), ForeignKey('questions.id'))
    question_9_id=Column(Integer(), ForeignKey('questions.id'))
    question_10_id=Column(Integer(), ForeignKey('questions.id'))
    question_11_id=Column(Integer(), ForeignKey('questions.id'))
    question_12_id=Column(Integer(), ForeignKey('questions.id'))
    question_13_id=Column(Integer(), ForeignKey('questions.id'))
    question_13_id=Column(Integer(), ForeignKey('questions.id'))
    question_15_id=Column(Integer(), ForeignKey('questions.id'))




