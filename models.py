import uuid
from sqlalchemy import ForeignKey, text
from extensions import db

def generate_id():
    return str(uuid.uuid4())[:6]


class Course(db.Model):
    __tablename__ = "course"
    course_code = db.Column(db.String(50), primary_key=True)
    course_name = db.Column(db.String(200), nullable=False)
    course_credits = db.Column(db.Float, nullable=False)

    distributions = db.relationship("GradeDistribution", back_populates="course")
    completions = db.relationship("Completed", back_populates="course")
    predictions = db.relationship("Prediction", back_populates="course")

class Student(db.Model):
    __tablename__ = "student"
    ku_id = db.Column(db.String(50), primary_key=True)
    major = db.Column(db.String(100), nullable=True)

    completions = db.relationship("Completed", back_populates="student")
    requests = db.relationship("PredictionRequest", back_populates="student")

class GradeDistribution(db.Model):
    __tablename__ = "grade_distribution"
    course_code = db.Column(
        db.String(50),
        db.ForeignKey("course.course_code", ondelete="CASCADE"),
        primary_key=True
    )
    grade_value = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer, primary_key=True)
    count = db.Column(db.Integer, nullable=False)

    course = db.relationship("Course", back_populates="distributions")

class Completed(db.Model):
    __tablename__ = "completed"
    ku_id = db.Column(
        db.String(50),
        ForeignKey("student.ku_id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True
    )

    course_code = db.Column(
        db.String(50),
        ForeignKey("course.course_code", ondelete="CASCADE"),
        primary_key=True
    )

    year = db.Column(db.Integer, primary_key=True)
    grade = db.Column(db.Integer, nullable=False)

    student = db.relationship("Student", back_populates="completions")
    course = db.relationship("Course", back_populates="completions")


class PredictionRequest(db.Model):
    __tablename__ = "prediction_request"
    request_id = db.Column(db.String(12), primary_key=True, default=generate_id)
    student_id = db.Column(
        db.String(50),
        ForeignKey("student.ku_id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False
    )

    request_date = db.Column(
        db.DateTime(timezone=True),
        server_default=text("timezone('Europe/Copenhagen', now())")
    )

    student = db.relationship("Student", back_populates="requests")
    predictions = db.relationship("Prediction", back_populates="request")

class Prediction(db.Model):
    __tablename__ = "prediction"
    request_id = db.Column(db.String(12), db.ForeignKey("prediction_request.request_id"), primary_key=True)
    course_code = db.Column(db.String(50), db.ForeignKey("course.course_code"), primary_key=True)
    predicted_grade = db.Column(db.Integer, nullable=False)
    z_score = db.Column(db.Float, nullable=True)

    request = db.relationship("PredictionRequest", back_populates="predictions")
    course = db.relationship("Course", back_populates="predictions")
