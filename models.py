from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, UniqueConstraint, Index
import uuid

def generate_id():
    return str(uuid.uuid4())[:6]

db = SQLAlchemy() 


class Course(db.Model):
    __tablename__ = "course"
    course_code = db.Column(db.String(50), primary_key=True)
    course_name = db.Column(db.String(200), nullable=False)
    course_credits = db.Column(db.Float, nullable=False)

    distributions = db.relationship("GradeDistribution", back_populates="course", cascade="all, delete-orphan")
    completions = db.relationship("Completed", back_populates="course", cascade="all, delete-orphan")
    predictions = db.relationship("Prediction", back_populates="course", cascade="all, delete-orphan")

class Student(db.Model):
    __tablename__ = "student"
    ku_id = db.Column(db.String(50), primary_key=True)
    major = db.Column(db.String(100), nullable=True)

    completions = db.relationship("Completed", back_populates="student", cascade="all, delete-orphan")
    requests = db.relationship("PredictionRequest", back_populates="student", cascade="all, delete-orphan")

class GradeDistribution(db.Model):
    __tablename__ = "grade_distribution"
    course_code = db.Column(db.String(50), db.ForeignKey("course.course_code"), primary_key=True)
    grade_value = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer, primary_key=True)
    count = db.Column(db.Integer, nullable=False)

    course = db.relationship("Course", back_populates="distributions")

class Completed(db.Model):
    __tablename__ = "completed"
    id = db.Column(db.Integer, primary_key=True)
    ku_id = db.Column(db.String(50), ForeignKey("student.ku_id"), nullable=False)
    course_code = db.Column(db.String(50), ForeignKey("course.course_code"), nullable=False)
    year = db.Column(db.Integer, nullable=True)
    grade = db.Column(db.Integer, nullable=False)

    student = db.relationship("Student", back_populates="completions")
    course = db.relationship("Course", back_populates="completions")
    __table_args__ = (UniqueConstraint("ku_id", "course_code", "year", name="uq_completed_unique"),)

class PredictionRequest(db.Model):
    __tablename__ = "prediction_request"
    request_id = db.Column(db.String(12), primary_key=True, default=generate_id, unique=True)
    student_id = db.Column(db.String(50), ForeignKey("student.ku_id"), nullable=False)
    request_date = db.Column(db.DateTime, server_default=db.func.now())
    student = db.relationship("Student", back_populates="requests")
    predictions = db.relationship("Prediction", back_populates="request", cascade="all, delete-orphan")

class Prediction(db.Model):
    __tablename__ = "prediction"
    id = db.Column(db.Integer, primary_key=True)
    request_id = db.Column(db.String(12), ForeignKey("prediction_request.request_id"), nullable=False)
    course_code = db.Column(db.String(50), ForeignKey("course.course_code"), nullable=False)
    predicted_grade = db.Column(db.Integer, nullable=False)
    confidence_score = db.Column(db.Float, nullable=True)

    request = db.relationship("PredictionRequest", back_populates="predictions")
    course = db.relationship("Course", back_populates="predictions")
    __table_args__ = (UniqueConstraint("request_id", "course_code", name="uq_request_course"),)
