import numpy as np
from sqlalchemy import select, text
import scipy.stats as ss
from app1 import PseudoCourse, db, app
from models import Course, GradeDistribution, Completed

#Percentile matching

f_grade_percentiles = []
grade_values = [-3, 0, 2, 4, 7, 10, 12]

def sql_get_dist(c: Course, year=2023):
    return text(f"SELECT TABLE grade_distribution d WHERE d.course_code ={c.course_code} AND d.year = {year}")

def get_dist(c: Course):
    cds = []
    cds.append(db.session.execute(sql_get_dist(c)))
    c.distributions = cds

def zipper2(p:PseudoCourse):
    cds = p.course.distributions
    grades = np.array([d.grade_value for d in cds])
    idx = np.argsort(grades)
    count = np.array([d.count for d in cds])[idx]
    return zip(grades, count)

def predict_grade(p: PseudoCourse, completed: list[PseudoCourse]):
    cdf_pred = get_cdf(zipper2(p))

    for comp in completed: get_dist(comp.course)

    completed_cdfs = [get_cdf(zipper2(comp)) for comp in completed]
    avg_percentile = np.mean([percentileFromGrade(c, p.cGrade) for c in completed_cdfs for p in completed])

    prediction = gradeFromPercentile(avg_percentile)
    p.cGrade = prediction

def get_cdf(fDistribution):
    total_students = sum([e[1] for e in fDistribution])
    arr = np.array([e[1]/total_students for e in fDistribution])
    cumulative = 0
    r = []
    for i in range(len(grade_values)):
        cumulative += arr[i]
        r.append(grade_values[i],arr[i],cumulative)
    return r

def percentileFromGrade(cdf: list, grade: int):
    return [e for e in cdf if e==grade]

def gradeFromPercentile(avgPct, pCourses):
    # find percentile matching grade for pCourses
    

 
