from datetime import date
from typing import Optional

from django.db import transaction
from django.utils import timezone

from testing_examples.models import School, Student
from testing_examples.selectors.schools import (
    school_list_school_courses,
)
from testing_examples.services.rosters import roster_create


@transaction.atomic
def student_create(*, email: str, school: School, start_date: Optional[date] = None) -> Student:
    student = Student(email=email, school=school)
    student.full_clean()
    student.save()

    start_date = start_date or timezone.now()

    school_courses = school_list_school_courses(school=school, start_date=start_date).select_related(
        "school_course__school"
    )

    for school_course in school_courses:
        roster_create(
            student=student, school_course=school_course, start_date=start_date, end_date=school_course.end_date
        )

    return student
