from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pandas as pd

from models import Answer, Question, Game, Player


engine = create_engine('sqlite:///database.db')
Session = sessionmaker(bind=engine)
session = Session()

df=pd.read_excel('../animals.xlsx')


def delete_records():
    session.query(Game).delete()
    
    session.query(Answer).delete()
    session.query(Player).delete()    
    session.query(Question).delete()
    session.commit()

def add_answers():
    answers=[Answer(answer="aardvark", category="animal"), 
                    Answer(answer="alpaca", category="animal"),
                    Answer(answer="baboon", category="animal"),
                    Answer(answer="badger", category="animal"),
                    Answer(answer="caribou", category="animal"),
                    Answer(answer="cheetah", category="animal"),
                    Answer(answer="donkey", category="animal"),
                    Answer(answer="dragonfly", category="animal"),
                    Answer(answer="earthworm ", category="animal"),
                    Answer(answer="egret", category="animal"),
                    Answer(answer="falcon", category="animal"),
                    Answer(answer="fox squirrel", category="animal"),
                    Answer(answer="giant isopod", category="animal"),
                    Answer(answer="horseshoe crab", category="animal"),
                    Answer(answer="moon jellyfish", category="animal"),
                    Answer(answer="kiwi", category="animal"),
                    Answer(answer="mink", category="animal"),
                    Answer(answer="olm", category="animal"),
                    Answer(answer="sea urchin", category="animal"),
                    Answer(answer="red-eyed tree frog.", category="animal"),
                    Answer(answer="venus flytrap", category="animal"),
                    Answer(answer="wallaby", category="animal"),
                    Answer(answer="yak", category="animal"),
                    Answer(answer="zebra", category="animal")]    
    for ans in answers:
        session.add(ans)
    session.commit()
    return answers

if __name__=='__main__':

    delete_records()
    test.drop()
    #add_answers()
    df.to_sql('answers', con=engine, if_exists='append', index=False)
