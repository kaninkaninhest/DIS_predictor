from flask import Flask, request, render_template, redirect, url_for, session
from models import Student, Course, Completed, Prediction, PredictionRequest
from sqlalchemy import select, func, delete, and_
from flask_migrate import Migrate
from dataclasses import dataclass
import predict
import re


cCodeRegExp = re.compile(r'[NL][A-Z]{3}\d{5}U\s*$', re.IGNORECASE)

gradesRegExp = re.compile(r'[0]*[-][0]*[3]\s*$' \
                          r'|[0]*(0|2|4|7|10|12)\s*$')

kuIDRegExp = re.compile(r'[a-z]{3}[0-9]{3}', re.IGNORECASE)

pseudo_completed = []
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
                add_completed(existing)
                add_predictions(existing)
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
            else: courseGrade=int(courseGrade)

            course = lookup_cid(courseId)
            if course: 
                sID = session.get('ku_id')
                stud = lookup_sid(sID)

                pseudo = PseudoCourse(course_name=course.course_name,
                                       course_code=course.course_code,
                                        grade=courseGrade)
                
                completed_course = Completed(
                                        ku_id=sID,
                                        course_code=course.course_code,
                                        year=2025,
                                        grade=courseGrade,
                                        student=stud,
                                        course=course
                                    )
                stud.completions.append(completed_course)
                db.session.add(completed_course)
                db.session.commit()
            else: pseudo=None

            if pseudo:
                b = False
                for e in pseudo_completed:
                    if e.course_code == pseudo.course_code:
                        pseudo_completed.remove(e) #if already finished, it can be overwritten
                for e in pred_courses: 
                    if e.course_code == pseudo.course_code:
                        b=True
                if not b: pseudo_completed.append(pseudo)


        elif form_type == "predict":
            courseId = request.form["courseId"]

            pred_course = lookup_cid(courseId)
            if pred_course:
                b = False
                for e in pseudo_completed:
                    if e.course_code == pred_course.course_code:
                        b=True
                if not b: 
                    sid = session.get('ku_id')
                    stud = lookup_sid(sid)

                    pseudo_pred = PseudoCourse(course_name=pred_course.course_name,
                                                course_code=pred_course.course_code,
                                                grade=None)
                    
                    predict.predict_grade(pseudo_pred, pseudo_completed, sid)
                    pred_courses.append(pseudo_pred)

        elif form_type == "clear":
            clear_data(lookup_sid(session.get('ku_id')))
            pred_courses.clear()
            pseudo_completed.clear()

        return redirect(url_for('index'))  # reload page

    return render_template("index.html",
                           pseudo_completed=pseudo_completed,
                           pred_courses=pred_courses)




@dataclass
class PseudoCourse:
    course_code: str
    course_name: str
    grade: int | None = None


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

    
def add_completed(student: Student):
    l = student.completions
    for e in l:
        pseudo_completed.append(PseudoCourse(course_name=e.course.course_name,
                                course_code=e.course.course_code,
                                grade=e.grade
                                ))
        
def add_predictions(student: Student):
    sid = student.ku_id

    stmt = (
        select(
            Prediction.predicted_grade,
            Prediction.course_code
        )
        .select_from(PredictionRequest)
        .join(Prediction, Prediction.request_id == PredictionRequest.request_id)
        .where(PredictionRequest.student_id == sid)
    )

    rows = db.session.execute(stmt).all()

    for predicted_grade, course_code in rows:
        course = lookup_cid(course_code)
        course_name = course.course_name if course is not None else course_code

        pred_courses.append(
            PseudoCourse(
                course_code=course_code,
                course_name=course_name,
                grade=predicted_grade
            )
        )

def clear_data(student: Student):
    sid = student.ku_id
    db.session.execute(
        delete(Prediction).where(
            Prediction.request_id.in_(
                select(PredictionRequest.request_id)
                .where(PredictionRequest.student_id == sid)
            )
        )
    )

    db.session.execute(
        delete(PredictionRequest).where(
            PredictionRequest.student_id == sid
        )
    )

    db.session.execute(
        delete(Completed).where(
            Completed.ku_id == sid
        )
    )

    db.session.commit()


if __name__ == '__main__':
    app.run(debug=True)
