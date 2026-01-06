from courses.models import Course
from core.exceptions.error_messages import ErrorCodes
from core.exceptions.exception import CustomApiException




def get_course_comments(course_id):
    course = Course.objects.filter(id=course_id, is_started=True).prefetch_related('feedbacks__user').first()
    if not course:
        raise CustomApiException(ErrorCodes.NOT_FOUND, message="Course not found")
    
    comments_data = []
    for comment in course.feedbacks.all():
        comments_data.append({
            "id": comment.id,
            "user_email": comment.user.email,
            "rating": comment.rating,
            "reaction": comment.reaction,
            "comment": comment.comment,
            "created_at": comment.created_datetime,
        })
    
    return {
        "course_id": course.id,
        "comments": comments_data,
    }