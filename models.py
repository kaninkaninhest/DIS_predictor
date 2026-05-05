from app import db
from app import generate_id
from sqlalchemy import ForeignKey


class Course(db.Model):
    course_name = db.Column(db.String(200))
    course_code = db.Column(db.String(200), primary_key=True)
    course_credits = db.Column(db.Int, nullable=False)

    def __init__(self, courseName, courseCode, courseCredits):
        self.course_code = courseCode
        self.course_name = courseName
        self.course_credits = courseCredits

class Student(db.Model):
    ku_id = db.Column(db.String(200), primary_key=True)
    major = db.Column(db.String(200), nullable=True)

    def __init__(self, ku_id, major):
        self.ku_id = ku_id
        self.major = major
        
        
class Has_Grade_Distribution(db.Model):
    grade_value = db.Column(db.Int, nullable=False)
    count = db.Column(db.Int, nullable=False)
    year = db.Column(db.Int, nullable=False)
    course_code = db.Column(db.String(200), ForeignKey(Course.course_code), nullable=False)

    def __init__(self, gradeval, count, year, course_code):
        self.grade_value = gradeval
        self.count = count
        self.year = year
        self.course_code = course_code
                
class Completed(db.Model): 
    year = db.Column(db.Int, nullable=True)
    act_grade = db.Column(db.Int, nullable=False)
    course_code = db.Column(db.String(200), ForeignKey(Course.course_code), nullable=False)
    ku_id = db.Column(db.String(200), ForeignKey(Student.ku_id), nullable=False)

    def __init__(self, year, act_grade, ku_id, course_code):
        self.act_grade = act_grade
        self.ku_id = ku_id
        self.year = year
        self.course_code = course_code

class Prediction_Request(db.Model):
    request_id = db.Column(db.String(6), primary_key=True, default=generate_id, unique=True)

class Predicts(db.Model):
    confidence_score = db.Column(db.Float, nullable=False)
    pred_grade = db.Column(db.Int, nullable=False)
    course_code = db.Column(db.String, ForeignKey(Prediction_Request.request_id), nullable=False)
    request_id = db.Column(db.String, ForeignKey(Prediction_Request.request_id), nullable=False)

    def __init__(self, confidence_score, pred_grade, course_code, request_id):
        self.confidence_score = confidence_score
        self.pred_grade = pred_grade
        self.course_code = course_code
        self.request_id = request_id