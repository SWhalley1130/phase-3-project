from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import random

import inquirer
import inquirer.themes
import simple_chalk as sc

from db.models import Answer, Question, Game, Player

basic=sc.green
warning=sc.red

def start_game():
    question=[inquirer.List(
            'returning_player', 
            message="Are you a returning player?", 
            choices=["Yes", "No"],
            )]
    resp=inquirer.prompt(question, theme=inquirer.themes.GreenPassion())

    if resp['returning_player']=="Yes":
        return True
    elif resp['returning_player']=="No":
        return False


def find_player():
    resp=input(basic("Welcome back! Please enter your username: "))
    current_player=session.query(Player).filter(Player.username==resp).first()
    if current_player==None:
        print(warning("I couldn't find that username in my system."))
        pass

    return current_player

def create_new_player():
    user=input(basic("Welcome to the game! Please enter a username.\n"))
    query=session.query(Player).filter(Player.username==user).first()
    if query!=None:
        print(warning("That username is already taken."))
        pass

    else:
        passw=input(basic("Please create a password: "))
        
        player=Player(username=user, password=passw)
        session.add(player)
        session.commit()
        return session.query(Player).filter(Player.username==user).first()

def log_in(player):
    passw=input(basic("Please enter your password: "))
    query = session.query(Player).filter(Player.username==player.username).first()
    if passw==query.password:
        print(basic("""
 _                       _   _      
| |___  __ _ __ _ ___ __| | (_)_ _  
| / _ \/ _` / _` / -_) _` | | | ' \ 
|_\___/\__, \__, \___\__,_| |_|_||_|
    |___/|___/              
        """))
        return True
    else:
        return False
    

def select_mode():
    if current_player.username=="admin":
        question=[
            inquirer.List(
                'mode', 
                message="What what you like to do?", 
                choices=["Play New Game", "Play Prior Game", "Edit Username", "Edit Password","Delete Account", "Edit Questions & Answers"],
                )]
    else:
        question=[
            inquirer.List(
                'mode', 
                message="What what you like to do?", 
                choices=["Play New Game", "Play Prior Game", "Edit Username", "Edit Password","Delete Account"],
                )]
    return inquirer.prompt(question, theme=inquirer.themes.GreenPassion())

    
#### generate_game does not currently implament a difficulty rating ####  
  
def generate_game():
    questions=[]
    while len(questions)<15:
        query=random.choice(session.query(Question).all())
        if query not in questions:
            questions.append(query)
    return questions

def play_round(question):
    answers=[]
    correct_answer=session.query(Answer).filter(Answer.id == question.answer_id).first()
    answers.append(correct_answer)
    while len(answers)<4:
        query=random.choice(session.query(Answer).all())
        if query not in answers:
            answers.append(query)
    random.shuffle(answers)
    round_question=[
        inquirer.List(
        'player_answer',
        message=question.question, 
        choices=[a for a in answers]
        )
    ]
    player_answer=inquirer.prompt(round_question, theme=inquirer.themes.GreenPassion())

    if player_answer['player_answer']==correct_answer:
        return True
    else:
        return False
    

def play_game(questions):
    print(basic("""
                          _            _          _ 
 __ _ __ _ _ __  ___   __| |_ __ _ _ _| |_ ___ __| |
/ _` / _` | '  \/ -_) (_-<  _/ _` | '_|  _/ -_) _` |
\__, \__,_|_|_|_\___| /__/\__\__,_|_|  \__\___\__,_|
|___/            
    """))

    possible_scores=["$0","$500", "$1,000", "$2,000","$3,000","$5,000","$7,500",
                     "$10,000","$15,000","$25,000","$50,000","$75,000",
                     "$150,000","$250,000","$500,000","$1,000,000"]

    current_player_score=0
    for q in questions:
        if play_round(q):
            current_player_score+=1
            
            print(basic(f"That's correct! Your score is {current_player_score}. "\
                       + f"This equates to {possible_scores[current_player_score]}."))
            q= [inquirer.List(
                'resp', 
                message="Would you like to continue?",
                choices=["Yes", "No"]
            )]

            yes_or_no=inquirer.prompt(q, theme=inquirer.themes.GreenPassion())
            if yes_or_no['resp']=="No":
                end_game(current_player_score, current_player, questions)
                exit()
        else: 
            print(warning(f"Oh no! That's incorrect. You're score was {current_player_score}. "\
                          +f"That would have earned you {possible_scores[current_player_score]}. "\
                            + "Better luck next time!"))
            end_game(current_player_score, current_player, questions)
            exit()
    
    end_game(current_player_score, current_player, questions)


def end_game(score, player, questions):
    game=Game(score=score, player_id=player.id, question_1_id=questions[0].id,question_2_id=questions[1].id,question_3_id=questions[2].id,
              question_4_id=questions[3].id, question_5_id=questions[4].id,question_6_id=questions[5].id,question_7_id=questions[6].id,
              question_8_id=questions[7].id,question_9_id=questions[8].id, question_10_id=questions[9].id,question_11_id=questions[10].id,
              question_12_id=questions[11].id,question_13_id=questions[12].id,question_14_id=questions[13].id, question_15_id=questions[14].id)
    session.add(game)
    session.commit()

def admin_edit_mode():
    q=[inquirer.List(
        "a",
        message="What would you like to do?",
        choices=["Edit Questions", "Edit Answers", "Add Question", "Add Answers"]
    )]
    resp=inquirer.prompt(q, theme=inquirer.themes.GreenPassion())
    if resp['a']=="Edit Questions":
        questions=session.query(Question).limit(5).all()
        q=[inquirer.Checkbox(
            'a',
            message="Please select which questions you'd like to edit.",
            choices=[quest.question for quest in questions]
        )]
        a=inquirer.prompt(q, theme=inquirer.themes.GreenPassion())






if __name__ == '__main__':
    engine = create_engine('sqlite:///db/database.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    print(basic("""
     /$$      /$$ /$$                       /$$      /$$                       /$$                    /$$$$$$$$              /$$$$$$$           
    | $$  /$ | $$| $$                      | $$  /$ | $$                      | $$                   |__  $$__/             | $$__  $$          
    | $$ /$$$| $$| $$$$$$$   /$$$$$$       | $$ /$$$| $$  /$$$$$$  /$$$$$$$  /$$$$$$   /$$$$$$$         | $$  /$$$$$$       | $$  \ $$  /$$$$$$ 
    | $$/$$ $$ $$| $$__  $$ /$$__  $$      | $$/$$ $$ $$ |____  $$| $$__  $$|_  $$_/  /$$_____/         | $$ /$$__  $$      | $$$$$$$  /$$__  $$
    | $$$$_  $$$$| $$  \ $$| $$  \ $$      | $$$$_  $$$$  /$$$$$$$| $$  \ $$  | $$   |  $$$$$$          | $$| $$  \ $$      | $$__  $$| $$$$$$$$
    | $$$/ \  $$$| $$  | $$| $$  | $$      | $$$/ \  $$$ /$$__  $$| $$  | $$  | $$ /$$\____  $$         | $$| $$  | $$      | $$  \ $$| $$_____/
    | $$/   \  $$| $$  | $$|  $$$$$$/      | $$/   \  $$|  $$$$$$$| $$  | $$  |  $$$$//$$$$$$$/         | $$|  $$$$$$/      | $$$$$$$/|  $$$$$$$
    |__/     \__/|__/  |__/ \______/       |__/     \__/ \_______/|__/  |__/   \___/ |_______/          |__/ \______/       |_______/  \_______/
                                                                                                                                                
                                                                                                                                                
                                                                                                                                                
    /$$$$$$        /$$      /$$ /$$ /$$ /$$ /$$                               /$$                     /$$$$                                   
    /$$__  $$      | $$$    /$$$|__/| $$| $$|__/                              |__/                    /$$  $$                                  
    | $$  \ $$      | $$$$  /$$$$ /$$| $$| $$ /$$  /$$$$$$  /$$$$$$$   /$$$$$$  /$$  /$$$$$$   /$$$$$$|__/\ $$                                  
    | $$$$$$$$      | $$ $$/$$ $$| $$| $$| $$| $$ /$$__  $$| $$__  $$ |____  $$| $$ /$$__  $$ /$$__  $$   /$$/                                  
    | $$__  $$      | $$  $$$| $$| $$| $$| $$| $$| $$  \ $$| $$  \ $$  /$$$$$$$| $$| $$  \__/| $$$$$$$$  /$$/                                   
    | $$  | $$      | $$\  $ | $$| $$| $$| $$| $$| $$  | $$| $$  | $$ /$$__  $$| $$| $$      | $$_____/ |__/                                    
    | $$  | $$      | $$ \/  | $$| $$| $$| $$| $$|  $$$$$$/| $$  | $$|  $$$$$$$| $$| $$      |  $$$$$$$  /$$                                    
    |__/  |__/      |__/     |__/|__/|__/|__/|__/ \______/ |__/  |__/ \_______/|__/|__/       \_______/ |__/                                    
                                                                                                                    
    """))

    current_player=None
    home_screen="selection"

    

    while current_player==None:
        if (start_game()):
            current_player=find_player()
        else:
            current_player=create_new_player()

    while log_in(current_player)==False:
        print(warning("That password is incorrect. Please try again."))
        pass


    while home_screen=="selection":
        answer=select_mode()
        if answer["mode"]=="Edit Username":
            if current_player.username!="admin":
                while current_player.edit_username(session)==False:
                    pass
                session.commit()
            else:
                print(warning("Cannot edit admin username."))
        elif answer["mode"]=="Edit Password":
            while current_player.edit_password()==False:
                pass
            session.commit()
        elif answer["mode"]=="Delete Account":
            if current_player.username!="admin":
                query=session.query(Player).filter(Player.username==current_player.username).first()
                games=session.query(Game).filter(Game.player_id==current_player.id).all()
                for g in games:
                    session.delete(g)
                session.delete(query)
                session.commit()
                print(basic("Thank you for playing! Please feel free to join again."))
                exit()
            else:
                print(warning("Cannot delete admin account."))
        elif answer["mode"]=="Play Prior Game":
            home_screen="play game"
            gamess=session.query(Game).order_by(Game.score).all()
            formatted=[f'ID: {g.id} Score: {g.score}, Player: {session.query(Player).filter(Player.id==g.player_id).first().username}' for g in gamess]
            q=[
                inquirer.List(
                'quiz_choice',
                message="Which game would you like to play?",
                choices=formatted
                )
            ]
            a=inquirer.prompt(q, theme=inquirer.themes.GreenPassion())
            index=formatted.index(a['quiz_choice'])
            questions=(gamess[index].question_list())
            questions=[session.query(Question).filter(Question.id==q).first() for q in questions]
            play_game(questions)
        elif answer["mode"]=="Edit Questions & Answers":
            admin_edit_mode()
        else: 
            home_screen="play game"


    questions=generate_game()
    play_game(questions)
        


