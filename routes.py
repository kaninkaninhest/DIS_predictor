from dataclasses import dataclass
import re

from flask import Blueprint, render_template, request, redirect, url_for, session
from sqlalchemy import select, func, delete

from models import Student, Course, Completed, Prediction, PredictionRequest, db
import services.prediction as predict

bp = Blueprint("main", __name__)

gradesRegExp = re.compile(r"^(?:-3|0|2|4|7|10|12)$")
kuIDRegExp = re.compile(r"^[a-z]{3}\d{3}$", re.IGNORECASE)


@dataclass
class PseudoCourse:
    course_code: str
    course_name: str
    grade: int | None = None


def lookup_cid(cId):
    if not cId:
        return None

    value = cId.strip()

    result = db.session.execute(
        select(Course).where(func.lower(Course.course_code) == value.lower())
    ).scalar_one_or_none()

    if result is None:
        result = db.session.execute(
            select(Course).where(func.lower(Course.course_name) == value.lower())
        ).scalar_one_or_none()

    return result


def lookup_sid(sId):
    if not sId:
        return None

    return db.session.execute(
        select(Student).where(func.lower(Student.ku_id) == sId.lower())
    ).scalar_one_or_none()


def load_state(student: Student):
    pseudo_completed = [
        PseudoCourse(
            course_name=e.course.course_name,
            course_code=e.course.course_code,
            grade=e.grade,
        )
        for e in student.completions
    ]

    stmt = (
        select(Prediction.predicted_grade, Prediction.course_code)
        .select_from(PredictionRequest)
        .join(Prediction, Prediction.request_id == PredictionRequest.request_id)
        .where(PredictionRequest.student_id == student.ku_id)
    )

    pred_courses = []
    rows = db.session.execute(stmt).all()

    for predicted_grade, course_code in rows:
        course = lookup_cid(course_code)
        course_name = course.course_name if course is not None else course_code

        pred_courses.append(
            PseudoCourse(
                course_code=course_code,
                course_name=course_name,
                grade=predicted_grade,
            )
        )

    return pseudo_completed, pred_courses


def clear_data(student: Student):
    sid = student.ku_id

    db.session.execute(
        delete(Prediction).where(
            Prediction.request_id.in_(
                select(PredictionRequest.request_id).where(
                    PredictionRequest.student_id == sid
                )
            )
        )
    )

    db.session.execute(
        delete(PredictionRequest).where(PredictionRequest.student_id == sid)
    )

    db.session.execute(delete(Completed).where(Completed.ku_id == sid))
    db.session.commit()


@bp.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        form_type = request.form.get("form_type")

        if form_type == "login":
            ku_id = request.form["ku_id"].strip()

            if not kuIDRegExp.fullmatch(ku_id):
                return redirect(url_for("main.login"))

            existing = lookup_sid(ku_id)
            if existing is None:
                existing = Student(ku_id=ku_id, major=None)
                db.session.add(existing)
                db.session.commit()

            session["ku_id"] = existing.ku_id
            return redirect(url_for("main.index"))

    return render_template("login.html")


@bp.route("/index", methods=["GET", "POST"])
def index():
    sid = session.get("ku_id")
    student = lookup_sid(sid)

    if student is None:
        return redirect(url_for("main.login"))

    if request.method == "POST":
        form_type = request.form.get("form_type")

        if form_type == "finished":
            course_id = request.form.get("courseId", "").strip()
            course_grade = request.form.get("courseGrade", "").strip()

            if not gradesRegExp.fullmatch(course_grade):
                return redirect(url_for("main.index"))

            course = lookup_cid(course_id)
            if course is not None:
                # Remove any old completion for the same student/course
                db.session.execute(
                    delete(Completed).where(
                        Completed.ku_id == student.ku_id,
                        Completed.course_code == course.course_code,
                    )
                )

                # Remove any prediction for the same course, because it is now completed
                db.session.execute(
                    delete(Prediction).where(
                        Prediction.course_code == course.course_code,
                        Prediction.request_id.in_(
                            select(PredictionRequest.request_id).where(
                                PredictionRequest.student_id == student.ku_id
                            )
                        ),
                    )
                )

                completed_course = Completed(
                    ku_id=student.ku_id,
                    course_code=course.course_code,
                    year=2025,
                    grade=int(course_grade),
                    student=student,
                    course=course,
                )
                db.session.add(completed_course)
                db.session.commit()

        elif form_type == "predict":
            course_id = request.form.get("courseId", "").strip()
            pred_course = lookup_cid(course_id)

            if pred_course is not None:
                pseudo_completed, pred_courses = load_state(student)

                already_completed = any(
                    e.course_code.lower() == pred_course.course_code.lower()
                    for e in pseudo_completed
                )
                already_predicted = any(
                    e.course_code.lower() == pred_course.course_code.lower()
                    for e in pred_courses
                )

                if not already_completed and not already_predicted and pseudo_completed:
                    pseudo_pred = PseudoCourse(
                        course_name=pred_course.course_name,
                        course_code=pred_course.course_code,
                        grade=None,
                    )
                    predict.predict_grade(pseudo_pred, pseudo_completed, student.ku_id)

        elif form_type == "clear":
            clear_data(student)

        return redirect(url_for("main.index"))

    pseudo_completed, pred_courses = load_state(student)
    return render_template(
        "index.html",
        pseudo_completed=pseudo_completed,
        pred_courses=pred_courses,
    )