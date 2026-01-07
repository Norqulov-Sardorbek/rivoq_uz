from courses.models import Course
from core.exceptions.error_messages import ErrorCodes
from core.exceptions.exception import CustomApiException



def get_course_modules(course_id):
    course = Course.objects.filter(id=course_id, is_started=True).prefetch_related('modules__lessons').first()
    if not course:
        raise CustomApiException(ErrorCodes.NOT_FOUND, message="Course not found")
    
    modules_data = []
    for module in course.modules.all():
        lessons_data = []
        for lesson in module.lessons.all():
            lessons_data.append({
                "id": lesson.id,
                "title": lesson.title,
                "order": lesson.order,
                "video_url": lesson.video_url,
                "duration": lesson.duration,
                "description": lesson.description,
                "code_source": lesson.code_source,
            })
        modules_data.append({
            "id": module.id,
            "title": module.title,
            "description": module.description,
            "lessons_count": module.lessons_count,
            "total_duration": module.total_duration,
            "lessons": lessons_data,
        })
    
    return {
        "course_id": course.id,
        "course_title": course.title,
        "module_count": course.modules.count(),
        "lesson_count": course.lessons_count,
        "course_duration": course.total_duration,
        "modules": modules_data,
    }