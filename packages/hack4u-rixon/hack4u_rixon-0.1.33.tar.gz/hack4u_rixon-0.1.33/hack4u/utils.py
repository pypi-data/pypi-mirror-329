#!/usr/bin/env python3

from hack4u.courses import courses

def total_duration():
    return sum(course.duracion for course in courses)


