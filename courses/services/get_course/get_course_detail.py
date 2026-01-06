from courses.models import Course, Module, Lesson, CourseComment, WhatWeOffer, WhoIsThisCourseFor
from core.exceptions.error_messages import ErrorCodes
from core.exceptions.exception import CustomApiException
from django.db.models import Avg, Sum

def get_course_detail(course_id):
    course = Course.objects.filter(id=course_id, is_started=True).prefetch_related('students', 'modules__lessons', 'feedbacks', 'students__in_lesson').first()
    if not course:
        raise CustomApiException(ErrorCodes.NOT_FOUND, message="Course not found")
    what_we_offer = WhatWeOffer.objects.filter(course_id=course.id)
    who_is_for_data = []
    if what_we_offer.exists():
        for item in what_we_offer:
            what_we_offer_data.append({
                "id": item.id,
                "title": item.title,
                "description": item.description,
            })
    who_is_for = WhoIsThisCourseFor.objects.filter(course_id=course.id)
    what_we_offer_data = []
    if who_is_for.exists():
        for item in who_is_for:
            who_is_for_data.append({
                "id": item.id,
                "title": item.title,
            })
    return {
        "id": course.id,
        "title": course.title,
        "description": course.description,
        "teachers": course.teachers,
        "image": course.image.url if course.image else None,
        "price": course.price,
        "is_free": course.is_free,
        "is_started": course.is_started,
        "students_enrolled": course.students.count(),
        "created_at": course.created_datetime,
        "lessons_count": course.lessons_count,
        "average_rating": course.average_rating,
        "duration": course.total_duration,
        "what_we_offer": what_we_offer_data ,
        "who_is_for": who_is_for_data ,
    }