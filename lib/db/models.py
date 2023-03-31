from sqlalchemy import ForeignKey, Column, Integer, String, MetaData
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import simple_chalk as sc


basic=sc.green
warning=sc.red

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

    def __repr__(self):
        return f'{self.answer}'
    
    def edit_answer(self, session):
        print(basic(f"The old answer is: {self.answer}\nThe question is set to: {session.query(Question).filter(Question.answer_id==self.id).first()}"))
        new_answer=input(basic("Please enter a new answer: "))
        self.answer=new_answer

class Question(Base):
    __tablename__='questions'

    id=Column(Integer(), primary_key=True)
    question=Column(String())
    difficulty=Column(Integer())
    category=Column(String())

    answer_id=Column(Integer(), ForeignKey('answers.id'))

    def __repr__(self):
        return f'{self.question}'
    
    def edit_question(self, session, editting, inp=None):
        if editting=="question":
            print(basic(f"The old question is: {self.question}\nThe answer is set to: {session.query(Answer).filter(Answer.id==self.answer_id).first()}"))
            new_question=input(basic("Please enter a new question: "))
            self.question=new_question
        elif editting=="answer_id":
            self.answer_id=inp


class Player(Base):
    __tablename__='players'

    id=Column(Integer(), primary_key=True)
    username=Column(String())
    password=Column(String())

    def __repr__(self):
        return f'Username: {self.username} ' \
                +  f'Password: {self.password}'
    
    def edit_username(self, session):
        new_username=input(basic("Please enter a new username: "))
        query=session.query(Player).filter(Player.username==new_username).first()
        if query!=None:
            print(warning("That username is already taken"))
            return False
        else:
            self.username=new_username
            return True

    def edit_password(self):
        new_password=input(basic("Please enter a new username: "))
        self.password=new_password
        return True

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
    question_14_id=Column(Integer(), ForeignKey('questions.id'))
    question_15_id=Column(Integer(), ForeignKey('questions.id'))

    def question_list(self):
        return [self.question_1_id, self.question_2_id,self.question_3_id,self.question_4_id,self.question_5_id,
                self.question_6_id,self.question_7_id,self.question_8_id,self.question_9_id,self.question_10_id,
                self.question_11_id,self.question_12_id,self.question_13_id,self.question_14_id,self.question_15_id]




