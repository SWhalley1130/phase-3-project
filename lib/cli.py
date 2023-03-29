from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db.models import Answer, Question, Game, Player

def start_game():
    resp=input(f"Welcome! Are you a returning player? y/n\n")
    while True:
        if resp.lower()==('y' or 'yes'):
            return True
        elif resp.lower()==('n' or 'no'):
            return False
        else:
            resp=input("Welcome! Are you a returning player? y/n\n")

def find_player():
    resp=input("Welcome back! What is your username?\n")
    current_player=session.query(Player).filter(Player.username==resp).first()
    if current_player==None:
        resp=input("I couldn't find that username in my system.\nDo you want to try again (1) or create a new profile? (2)\n")
        if resp=='2': 
            create_new_player()
        else: 
            find_player()

    return current_player

def create_new_player():
    user=input("Welcome to the game! Please enter a username.\n")
    query=session.query(Player).filter(Player.username==user).first()
    if query!=None:
        print("That username is already taken.")
        create_new_player()
    passw=input("Please enter a password: ")
    
    player=Player(username=user, password=passw)
    session.add(player)
    session.commit()

    return session.query(Player).filter(Player.username==user).first()













if __name__ == '__main__':
    engine = create_engine('sqlite:///db/database.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    print("""
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
                                                                                                                    
    """)

    current_player=None

    if (start_game()):
        current_player=find_player()
    else:
        current_player=create_new_player()

    print(current_player.username)