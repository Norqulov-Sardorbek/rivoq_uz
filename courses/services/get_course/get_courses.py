from courses.models import Course


def get_courses():
    courses = Course.objects.filter(is_started=True)
    
    data = []
    for course in courses:
        data.append({
            "id": course.id,
            "title": course.title,
            "image": course.image.url if course.image else None,
        })
    return data
    