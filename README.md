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

## 2) How to interact with the grade predictor
Users start on a login page where they are prompted to enter their KU-ID. After submission, they are redirected to the main Grade Predictor page.

On the main page, the workflow is structured in two steps. First, the user must enter their completed courses along with the corresponding grades. This step is required before any predictions can be made. Once completed courses have been added, the user can proceed to the right-hand column, where they can enter courses they want grade predictions for.

Courses can be identified using either the full course name or the course code in both columns.

If the user wants to reset their session and remove all stored data associated with their KU-ID, they can use the “clear” button located in the top-right corner of the page.

## 3) ER-diagram and AI-declaration
  - The ERD can be found as a png named "predictor_er_diagram.png".
  - AI-declaration can be found as txt file named "AI_declaration.txt".