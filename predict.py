import numpy as np
import scipy.stats as ss
from app1 import PseudoCourse
from app1 import grade_values

#Percentile matching

f_grade_percentiles = []

def get_cdf(fDistribution):
    total_students = sum([e.count for e in fDistribution])
    arr = np.array([e/total_students for e in grade_values.copy()])
    cumulative = 0
    r = []
    for i in range(len(grade_values)):
        cumulative += arr[i]
        r.append(grade_values[i],arr[i],cumulative)
    return r

def percentileFromGrade(cdf: list, grade: int):
    return [e for e in cdf if e==grade]

def gradeFromPercentile(fCourses, pCourses):
    mean = np.mean(f_grade_percentiles)
 
