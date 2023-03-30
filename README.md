image.png

## Introduction

Thank you for reading me! This project was built using python 3.8.13 and pip 23.0.1. This is my CLI project for phase 3 of the Flatiron School. During this phase I learned python, sql, the concepts of ORM, sqlalchemy, and alembic. In addition to using these technologies and concepts, I used the simple-chalk and inquirer libraries for styling and choice selection, respectively. 

## Installation 

Use the package manager pip to install all needed dependencies for the game. Libraries include [sqlalchemy](https://www.sqlalchemy.org/), [alembic](https://alembic.sqlalchemy.org/en/latest/), [inquirer](https://python-inquirer.readthedocs.io/en/latest/), and [simple-chalk](https://pypi.org/project/simple-chalk/). 

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