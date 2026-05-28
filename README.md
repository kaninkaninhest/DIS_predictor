Grade predictor, based on prior courses

    DIS PROJECT 2026
    DIKU
    Marcus Fennestad (mpw603),
    Jacob Daniel Taarnberg (pkz685) 
    & Rasmus Appelby Kallehave(zwt566)


# Grade Predictor

## Requirements
- Python 3.13 (other versions might also work but this is what we used)
- PostgreSQL
- A terminal / command prompt

## 1) Setup

  # 1.1)Create database
(in terminal)

    createdb coursegrades_api
    psql -U postgres -d coursegrades_api -f coursegrades_dump.sql

  # 1.2)Create and activate a virtual environment

    python -m venv .venv

    .venv/bin/activate        #Mac/Linux
 
    .venv\Scripts\activate    #Windows

    python -m pip install --upgrade pip
    python -m pip install -r requirements.txt

  # 1.3) Run the app
    python app1.py

  # 1.4) Verify installed packages have compatible dependencies
    python -m pip check