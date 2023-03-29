from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pandas as pd

from models import Answer, Question, Game, Player


engine = create_engine('sqlite:///database.db')
Session = sessionmaker(bind=engine)
session = Session()

def delete_records():
    session.query(Game).delete()
    
    session.query(Answer).delete()
    session.query(Player).delete()    
    session.query(Question).delete()
    session.commit()

def add_answers():
    df=pd.read_excel('../answers.xlsx')
    df.to_sql('answers', con=engine, if_exists='append', index=False)


def add_questions():
    df=pd.read_excel('../questions.xlsx')
    df.to_sql('questions', con=engine, if_exists='append', index=False)

def create_admin_player():
    player=Player(username="sarah", password="admin")
    session.add(player)
    session.commit()


if __name__=='__main__':

    delete_records()
    add_answers()
    add_questions()
    create_admin_player()
    
