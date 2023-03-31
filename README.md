![alt text](/main_img.PNG)

## Introduction

Thank you for reading me! This project was built using python 3.8.13 and pip 23.0.1. This is my CLI project for phase 3 of the Flatiron School. During this phase I learned python, sql, the concepts of ORM, sqlalchemy, and alembic. In addition to using these technologies and concepts, I used the simple-chalk and inquirer libraries for styling and choice selection, respectively. The database is seeded using .xlxs files, which are read using pandas and openpyxl. 

## Installation 

Use the package manager pip to install all needed dependencies for the game. Libraries include [sqlalchemy](https://www.sqlalchemy.org/), [alembic](https://alembic.sqlalchemy.org/en/latest/), [inquirer](https://python-inquirer.readthedocs.io/en/latest/), [simple-chalk](https://pypi.org/project/simple-chalk/), [pandas](https://pypi.org/project/pandas/), and [openpyxl](https://pypi.org/project/openpyxl/). 

```bash
pip install
```

## Playing the game 

If you'd like to start your game using the seed data only, cd into /lib/db and run the seeds file from the pipenv shell.

```bash

# ./lib/db
python seeds.py
```

When you are ready to play the game, cd into the lib directory and run cli.py. 

```bash
#./lib 
python cli.py
```

![alt text](/log_in_img.PNG)

The player will be able to log in with a username and password (or create an account), and have the options to play a randomized game, play prior games (from themselves or other players), edit their username/password, delete their account, or quit. If a player is logged in as the admin, they also have the ability to edit/add/delete questions and answers. These options will be displayed after the player has logged in, on the select menu. The default username and password for the admin is 'admin'. Admin account cannot be deleted, it's username cannot be changed, but it's password can be updated. 

![alt text](/game_play.PNG)

Each game has 15 questions, with the option to quit in between questions. The highest score possible is 15. If a player gets a question wrong, the game is over. If the player correctly answers all questions or opts out of the game, the game is over. Currently, there is no distinction between winning and losing aside from the text that is shown at the end of the game. When a game ends, the questions, player, and score are all stored in the database and can be replayed by using 'Play Prior Game' from the select menu. 