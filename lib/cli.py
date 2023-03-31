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
    print(sc.black.bold.bgGreen(""" SELECT SCREEN """))
    if current_player.username=="admin":
        question=[
            inquirer.List(
                'mode', 
                message="What what you like to do?", 
                choices=["Play New Game", "Play Prior Game", "Edit Username", "Edit Password","Delete Account", "Quit","Edit Questions & Answers"],
                )]
    else:
        question=[
            inquirer.List(
                'mode', 
                message="What what you like to do?", 
                choices=["Play New Game", "Play Prior Game", "Edit Username", "Edit Password","Quit","Delete Account"],
                )]
    return inquirer.prompt(question, theme=inquirer.themes.GreenPassion())

    
#### generate_game does not currently implement a difficulty rating or category ####  
  
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


## The following function is terrible. It more or less works, but should be refactored 

def admin_edit_mode():
    print(sc.black.bold.bgGreen(""" ADMIN EDIT SCREEN """))
    print(sc.yellow("You may always reset the database to it's default settings. Please see the README."))
    q=[inquirer.List(
        "a",
        message="What would you like to do?",
        choices=["Edit Questions", "Edit Answers", "Add Question", "Add Answer", "Delete Question(s)", "Delete Answer(s)", "Exit Edit Mode"]
    )]
    resp=inquirer.prompt(q, theme=inquirer.themes.GreenPassion())
    if resp['a']=="Edit Questions":
        all_questions=session.query(Question).all()
        q=[inquirer.Checkbox(
            'a',
            message="Please select which questions you'd like to edit.",
            ##Checkbox allows a tuple: the first value is what is displayed, the second value is what is stored
            choices=[((f' {quest.question}, answer: {session.query(Answer).filter(Answer.id==quest.id).first()}'),quest.id) for quest in all_questions]
        )]
        questions_to_edit=inquirer.prompt(q, theme=inquirer.themes.GreenPassion())
        questions_to_edit=[get_object(quest, "question") for quest in questions_to_edit['a']]
        for q in questions_to_edit:
            q.edit_question(session, "question")
        session.commit()
    elif resp['a']=="Edit Answers":
        all_answers=session.query(Answer).all()
        q=[inquirer.Checkbox(
            'a',
            message="Please select which answers you'd like to edit.",
            choices=[((f' {ans.answer}, question: {session.query(Question).filter(Question.answer_id==ans.id).first()}'), ans.id) for ans in all_answers]
        )]
        answers_to_edit=inquirer.prompt(q, theme=inquirer.themes.GreenPassion())
        answers_to_edit=[get_object(ans, "answer") for ans in answers_to_edit['a']]        
        for a in answers_to_edit:
            a.edit_answer(session) 
        session.commit()

    elif resp['a']=='Add Question':
        print(basic("In it's current state, this game is not implementing it's category or difficulty settings. For now, the default are:"))
        print(basic("Category: Animal; Difficulty: 1"))
        new_q=input(basic("Please type your question: "))
        corresponding_a=input(basic("Now type it's answer: "))

        a_query=session.query(Answer).filter(Answer.answer==corresponding_a).first()
        q_query=session.query(Question).filter(Question.question==new_q).first()

        if q_query!=None:
            print(warning("That question is already in use."))
            pass

        if a_query==None:
            ans=Answer(answer=corresponding_a,category="animal")
            session.add(ans)
            session.commit()
            new_a_id=session.query(Answer).order_by(Answer.id.desc()).first()
        else:
            corr_a_id=session.query(Answer).filter(Answer.answer==corresponding_a).first()

        if q_query==None:
            if a_query==None:
                ques=Question(question=new_q, difficulty=1, category="animal", answer_id=new_a_id.id)
            else:
                ques=Question(question=new_q, difficulty=1, category="animal", answer_id=corr_a_id.id)
            session.add(ques)
            session.commit()
            
    elif resp['a']=='Add Answer':
        print(basic("In it's current state, this game is not implementing it's category or difficulty (for question) settings. For now, the default are:"))
        print(basic("Category: Animal; Difficulty: 1"))
        print(sc.yellow("Note that you can edit a question's answer in this mode. To do so, type in the new answer and the existing question that should now point to it."))
        new_a=input(basic("Please type your answer: "))
        corresponding_q=input(basic("Now type it's question: "))

        q_query=session.query(Question).filter(Question.question==corresponding_q).first()
        a_query=session.query(Answer).filter(Answer.answer==new_a).first()

        if a_query!=None:
            print(warning("That answer is already in use."))
            pass
        else:
            ans=Answer(answer=new_a, category="animal")
            session.add(ans)
            session.commit()
            new_a_id=session.query(Answer).order_by(Answer.id.desc()).first()
            if q_query==None:
                ques=Question(question=corresponding_q, category="animal", difficulty=1, answer_id=new_a_id.id)
                session.add(ques)
            else:
                q_query.edit_question(session, "answer_id", new_a_id.id)
            session.commit()

    elif resp['a']=="Delete Question(s)":
        all_questions=session.query(Question).all()
        q=[inquirer.Checkbox(
            'a',
            message="Please select which questions you'd like to edit.",
            choices=[((f' {quest.question}, answer: {session.query(Answer).filter(Answer.id==quest.id).first()}'),quest.id) for quest in all_questions]
        )]
        questions_to_edit=inquirer.prompt(q, theme=inquirer.themes.GreenPassion())
        questions_to_edit=[get_object(quest, "question") for quest in questions_to_edit['a']]
        for q in questions_to_edit:
            session.delete(q)
        session.commit()

    elif resp['a']=="Delete Answer(s)":
        print(warning("If you delete an answer that a question was associated with, that question will also be deleted."))
        all_answers=session.query(Answer).all()
        q=[inquirer.Checkbox(
            'a',
            message="Please select which answers you'd like to edit.",
            choices=[((f' {ans.answer}, question: {session.query(Question).filter(Question.answer_id==ans.id).first()}'), ans.id) for ans in all_answers]
        )]
        answers_to_edit=inquirer.prompt(q, theme=inquirer.themes.GreenPassion())
        answers_to_edit=[get_object(ans, "answer") for ans in answers_to_edit['a']]        
        for a in answers_to_edit:
            print(a.id)
            query=session.query(Question).filter(Question.answer_id==a.id).all()
            for i in query:
                session.delete(i)
            session.delete(a)
        session.commit()

    if resp['a']=='Exit Edit Mode':
        pass


def get_object(obj_id, type):
    if type=="question":
        return session.query(Question).filter(Question.id==obj_id).first()
    elif type=="answer":
        return session.query(Answer).filter(Answer.id==obj_id).first()

    






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
            gamess=session.query(Game).order_by(Game.score).all()
            if len(gamess)==0:
                print(warning("No prior games to choose from."))
            else:
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
        elif answer["mode"]=="Quit":
            print(basic("Thank you for playing!"))
            exit()
        else: 
            home_screen="play game"


    questions=generate_game()
    play_game(questions)
        


