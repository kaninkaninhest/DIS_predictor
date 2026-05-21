import numpy as np
from sqlalchemy import select
from app1 import PseudoCourse, db, app, lookup_sid
from models import GradeDistribution, Prediction, PredictionRequest


GRADE_VALUES = [-3, 0, 2, 4, 7, 10, 12]

def make_prediction_req(sid, pred_course, completed):
    # request can only be made if there are courses to predict on
    # and courses to predict for
    if completed and pred_course:
        stud = lookup_sid(sid)
        return PredictionRequest(student_id=sid, student=stud)
    else: return None

def get_dist(course_code, year=2023):
    return (
        db.session.execute(
            select(GradeDistribution).where(
                GradeDistribution.course_code == course_code,
                GradeDistribution.year == year
            )
        )
        .scalars()
        .all()
    )


def course_stats(distribution_rows):
    rows = sorted(distribution_rows, key=lambda r: r.grade_value)

    grades = np.array([r.grade_value for r in rows], dtype=float)
    counts = np.array([r.count for r in rows], dtype=float)

    total = counts.sum()
    if total == 0:
        return 0.0, 1.0

    mu = np.average(grades, weights=counts)
    variance = np.average((grades - mu) ** 2, weights=counts)
    sigma = float(np.sqrt(variance))

    if sigma == 0:
        sigma = 1.0

    return float(mu), sigma


def to_zscore(grade, mu, sigma):
    return (float(grade) - mu) / sigma


def from_zscore(z, mu, sigma):
    return mu + z * sigma


def nearest_legal_grade(x):
    return min(GRADE_VALUES, key=lambda g: abs(g - x))


def predict_grade(pred_course, completed, sid):
    req = make_prediction_req(sid, pred_course, completed)
    if req:
    # add prediction request to database
        db.session.add(req)
        db.session.commit()  
    
    z_scores = []

    for comp in completed:
        rows = get_dist(comp.course_code)
        mu, sigma = course_stats(rows)
        z_scores.append(to_zscore(comp.grade, mu, sigma))

    if not z_scores:
        raise ValueError("No completed courses to base prediction on")

    avg_z = float(np.mean(z_scores))

    target_rows = get_dist(pred_course.course_code)
    target_mu, target_sigma = course_stats(target_rows)

    raw_prediction = from_zscore(avg_z, target_mu, target_sigma)
    pred_course.grade = nearest_legal_grade(raw_prediction)

    pred = Prediction(
                      request_id=req.request_id,
                      course_code=pred_course.course_code,
                      predicted_grade=pred_course.grade,
                      z_score=avg_z
                    )
    db.session.add(pred)
    db.session.commit()

    return pred_course.grade