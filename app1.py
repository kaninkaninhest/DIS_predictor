from flask import Flask, request, render_template, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select, func, insert
from flask_migrate import Migrate
import re
import models
import predict
from models import Student, Course, Completed, PredictionRequest, Prediction, GradeDistribution


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

@app.route("/", methods=['GET','POST'])
def login():
    if request.method == "POST":
        form_type = request.form.get("form_type")
        if form_type == "login":
            ku_id = request.form["ku_id"].strip()
            if not kuIDRegExp.match(ku_id):
                return redirect("/login.html")

            existing = lookup_sid(ku_id)
            if existing:
                #if it exists retrieve finished courses from db
                pseudo_courses.extend(completed2pseudo(existing.completions))
            else:
                s = Student(ku_id=ku_id, major=None)
                db.session.add(s)
                db.session.commit()
                existing = s

            # store logged in student in Flask session
            session['ku_id'] = existing.ku_id

            return redirect(url_for('index'))

    return render_template("login.html")


@app.route("/index", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        form_type = request.form.get("form_type")
        if form_type == "finished":
            courseId = request.form["courseId"]
            courseGrade = request.form["courseGrade"]
            if not gradesRegExp.match(courseGrade): courseId="invalid"

            course = lookup_cid(courseId)
            if course: 
                sID = session.get('ku_id')
                stud = lookup_sid(sID)
                pseudo = PseudoCourse(course.course_name, courseGrade, course)
                completed_course = Completed(ku_id=sID,
                                   course_code=course.course_code,
                                   year=2025,
                                   grade=courseGrade,
                                   student=stud,
                                   course=course)
                stud.completions.append(completed_course)
                db.session.add(completed_course)
                db.session.commit()
            else: pseudo=None

            if pseudo:
                b = False
                for e in pseudo_courses:
                    if e.course.course_code == pseudo.course.course_code:
                        pseudo_courses.remove(e) #if already finished, it can be overwritten
                for e in pred_courses: 
                    if e.course.course_code == pseudo.course.course_code:
                        b=True
                if not b: pseudo_courses.append(pseudo)


        elif form_type == "predict":
            courseId = request.form["courseId"]

            pred_course = lookup_cid(courseId)
            if pred_course:
                b = False
                for e in pseudo_courses:
                    if e.course.course_code == pred_course.course_code:
                        b=True
                if not b: 
                    stud = lookup_sid(sID)
                    pseudo_pred = PseudoCourse(pred_course.course_name, None, pred_course)
                    predict.get_dist(pseudo_pred.course)
                    predict.predict_grade(pseudo_pred, pseudo_courses)
                    pred_courses.append(pseudo_pred)
                    
                    req = make_prediction_req()
                    if req:
                        # add prediction request to database
                        db.session.add(req)
                        db.session.commit()

        return redirect(url_for('index'))  # reload page

    return render_template("index.html", pseudo_courses=pseudo_courses, pred_courses=pred_courses)


def make_prediction_req():
    # request can only be made if there are courses to predict on
    # and courses to predict for
    if pseudo_courses and pred_courses:
        sID = session.get('ku_id')
        stud = lookup_sid(sID)
        return PredictionRequest(student_id=sID, student=stud)   
    else: return None

class PseudoCourse:
    def __init__(self, cName, cGrade, course: models.Course):
        self.cName = cName 
        self.cGrade = cGrade 
        self.course = course

    def __str__(self):
        return f"{self.cName}: {self.cGrade}"
    
def completed2pseudo(cs: list[Completed]):
    res = []
    for e in cs:
        res.append(PseudoCourse(e.course.course_name,
                                e.grade,
                                e.course))
    return res

def lookup_cid(cId):
    if cId is None:
        return None

    result = db.session.execute(
        select(Course).where(func.lower(Course.course_code) == cId.lower())
    ).scalar_one_or_none()

    if result == None: 
        result = db.session.execute(
        select(Course).where(func.lower(Course.course_name) == cId.lower())
    ).scalar_one_or_none()

    return result

def lookup_sid(sId):
    if sId is None:
        return None
    result = db.session.execute(
        select(Student).where(func.lower(Student.ku_id) == sId.lower())
    ).scalar_one_or_none()
    return result

if __name__ == '__main__':
    app.run(debug=True)
