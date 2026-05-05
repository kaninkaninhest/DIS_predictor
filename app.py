from flask import Flask, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select, func, insert
from flask_migrate import Migrate
import numpy as np
import re

cCodeRegExp = re.compile(r'[NL][A-Z]{3}\d{5}U\s*$', re.IGNORECASE)

gradesRegExp = re.compile(r'[0]*[-][0]*[3]\s*$' \
                          r'|[0]*(0|2|4|7|10|12)\s*$')

grade_fields = [
        "minusThree_Grade",
        "zero_Grade",
        "two_Grade",
        "four_Grade",
        "seven_Grade",
        "ten_Grade",
        "twelve_Grade"
    ]
grade_values = np.array([-3, 0, 2, 4, 7, 10, 12])

pseudo_courses = []
pred_courses = []

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123@localhost:5432/CourseGrades_api'

db = SQLAlchemy(app)

migrate = Migrate(app,db)


class Course(db.Model):
    courseName = db.Column(db.String(200), nullable=True)
    courseCode = db.Column(db.String(200), nullable=True, primary_key=True)

    minusThree_Grade = db.Column(db.Integer, nullable=False)
    zero_Grade = db.Column(db.Integer, nullable=False)
    two_Grade = db.Column(db.Integer, nullable=False)
    four_Grade = db.Column(db.Integer, nullable=False)
    seven_Grade = db.Column(db.Integer, nullable=False)
    ten_Grade = db.Column(db.Integer, nullable=False)
    twelve_Grade = db.Column(db.Integer, nullable=False)

    def __init__(self, courseName, courseCode, minusThree_Grade, zero_Grade, two_Grade, four_Grade, seven_Grade, ten_Grade, twelve_Grade):
        self.courseName = courseName
        self.courseCode = courseCode
        self.minusThree_Grade = minusThree_Grade
        self.zero_Grade = zero_Grade
        self.two_Grade = two_Grade
        self.four_Grade = four_Grade
        self.seven_Grade = seven_Grade
        self.ten_Grade = ten_Grade
        self.twelve_Grade = twelve_Grade



def predict_grade(c: Course):
    if not pseudo_courses: return "cannot predict based on provided data"
    else: 
        counts = [getattr(c, g) for g in grade_fields]
        gs = []
        pass


@app.route("/add_course.html", methods=['GET', 'POST'])
def add_course():
    if request.method == "POST":
        validAmount = re.compile(r'[0]*\d*')
        form_type = request.form.get("form_type")
        if form_type == "finished":
            courseCode = request.form["addCCode"]
            courseName = request.form["addCName"]
            if not cCodeRegExp.match(courseCode) or not courseName: 
                return redirect("/add_course.html")

            gs = []
            for i in range(len(grade_values)):
                val = request.form.get("addCGrade" + str(i), "")
                if val == "":
                    gs.append(0)
                else:
                    try:
                        gs.append(int(val))
                    except ValueError:
                        print("Inserted value not an integer")
                        gs.append(0)

            existing = db.session.execute(
                select(Course).where(func.lower(Course.courseCode) == courseCode.lower())
            ).scalar_one_or_none()

            if existing:
                print("Course already present")
                return redirect("/add_course.html")

            c = Course(courseName, courseCode, gs[0],gs[1], gs[2], gs[3], gs[4], gs[5], gs[6])
            db.session.add(c)
            db.session.commit()

    return render_template('add_course.html')


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
                    pred_grade = predict_grade(pseudo_pred.course)
                    pseudo_pred.cGrade = pred_grade
                    pred_courses.append(pseudo_pred)
        
            

        return redirect("/")  # reload page

    return render_template("index.html", pseudo_courses=pseudo_courses, pred_courses=pred_courses)

class PseudoCourse:
    def __init__(self, cName, cGrade, course: Course):
        self.cName = cName 
        self.cGrade = cGrade 
        self.course = course

    def __str__(self):
        return f"{self.cName}: {self.cGrade}"

def lookup_name(cId):
    if cId is None:
        return None

    result = db.session.execute(
        select(Course).where(func.lower(Course.courseCode) == cId.lower())
    ).scalar_one_or_none()

    if result == None: 
        result = db.session.execute(
        select(Course).where(func.lower(Course.courseName) == cId.lower())
    ).scalar_one_or_none()

    return result

if __name__ == '__main__':
    app.run(debug=True)
