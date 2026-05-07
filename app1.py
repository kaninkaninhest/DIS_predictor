from flask import Flask, request, render_template, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select, func, insert
from flask_migrate import Migrate
import re
import models
import predict


cCodeRegExp = re.compile(r'[NL][A-Z]{3}\d{5}U\s*$', re.IGNORECASE)

gradesRegExp = re.compile(r'[0]*[-][0]*[3]\s*$' \
                          r'|[0]*(0|2|4|7|10|12)\s*$')

kuIDRegExp = re.compile(r'[a-z]{3}[0-9]{3}', re.IGNORECASE)

pseudo_courses = []
pred_courses = []

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123@localhost:5432/CourseGrades_api'

from models import db
db.init_app(app)

migrate = Migrate(app, db)

app.secret_key = "123"

@app.route("/login.html", methods=['GET','POST'])
def login():
    if request.method == "POST":
        form_type = request.form.get("form_type")
        if form_type == "login":
            ku_id = request.form["ku_id"].strip()
            if not kuIDRegExp.match(ku_id):
                return redirect("/login.html")

            existing = db.session.execute(
                select(models.Student).where(func.lower(models.Student.ku_id) == ku_id.lower())
            ).scalar_one_or_none()

            if not existing:
                s = models.Student(ku_id, None)
                db.session.add(s)
                db.session.commit()
                existing = s

            # store logged in student in Flask session
            session['ku_id'] = existing.ku_id

            return redirect(url_for('index'))

    return render_template("login.html")


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        form_type = request.form.get("form_type")
        if form_type == "finished":
            courseId = request.form["courseId"]
            courseGrade = request.form["courseGrade"]
            if not gradesRegExp.match(courseGrade): courseId="invalid"

            course = lookup_name(courseId)
            if course is not None: 
                pseudo = PseudoCourse(course.courseName, courseGrade, course)
            else: pseudo=None

            if pseudo:
                b = False
                for e in pseudo_courses:
                    if e.course.courseCode == pseudo.course.courseCode:
                        b=True
                for e in pred_courses: 
                    if e.course.courseCode == pseudo.course.courseCode:
                        b=True
                if not b: pseudo_courses.append(pseudo)
        elif form_type == "predict":
            courseId = request.form["courseId"]

            pred_course = lookup_name(courseId)
            if pred_course:
                b = False
                for e in pseudo_courses:
                    if e.course.courseCode == pred_course.courseCode:
                        b=True
                if not b: 
                    pseudo_pred = PseudoCourse(pred_course.courseName, None, pred_course)
                    pred_grade = predict.predict_grade(pseudo_pred.course)
                    pseudo_pred.cGrade = pred_grade
                    pred_courses.append(pseudo_pred)
        
            

        return redirect("/")  # reload page

    return render_template("index.html", pseudo_courses=pseudo_courses, pred_courses=pred_courses)

class PseudoCourse:
    def __init__(self, cName, cGrade, course: models.Course):
        self.cName = cName 
        self.cGrade = cGrade 
        self.course = course

    def __str__(self):
        return f"{self.cName}: {self.cGrade}"

def lookup_name(cId):
    if cId is None:
        return None

    result = db.session.execute(
        select(models.Course).where(func.lower(models.Course.courseCode) == cId.lower())
    ).scalar_one_or_none()

    if result == None: 
        result = db.session.execute(
        select(models.Course).where(func.lower(models.Course.courseName) == cId.lower())
    ).scalar_one_or_none()

    return result

if __name__ == '__main__':
    app.run(debug=True)
