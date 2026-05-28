# Grade predictor

### DIS PROJECT 2026
### DIKU
    Marcus Fennestad (mpw603),
    Jacob Daniel Taarnberg (pkz685) 
    & Rasmus Appelby Kallehave(zwt566)


# Grade Predictor

## Requirements
- Python 3.12 (other versions might also work but this is what we used)
- PostgreSQL
- A terminal / command prompt

## 1) Setup

  ### 1.1)Create database

    createdb -U CourseGrades_api
    psql -U postgres -d CourseGrades_api -f coursegrades_dump.sql

  ### 1.2)Create and activate a virtual environment

    py -3.12 -m venv .venv

    .venv/bin/activate        #Mac/Linux
 
    .venv\Scripts\activate    #Windows

    python -m pip install --upgrade pip
    python -m pip install -r requirements.txt

  ### 1.3) Configure PostgreSQL credentials
Before running the application, set your PostgreSQL password as an environment variable.


Windows (PowerShell)
    
    $env:DB_PASSWORD="your_postgres_password"


macOS / Linux
    
    export DB_PASSWORD="your_postgres_password"

Optional environment variables:

    DB_USER (default: postgres)
    DB_HOST (default: localhost)
    DB_PORT (default: 5432)
    DB_NAME (default: CourseGrades_api)

  ### 1.4) Verify installed packages have compatible dependencies
    python -m pip check

  ### 1.5) Run the app
    python app1.py

## 2) ER-diagram and AI-declaration
  - The ERD can be found as a png named "predictor_er_diagram.png".
  - AI-declaration can be found as txt file named "AI_declaration.txt".