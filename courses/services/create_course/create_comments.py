from courses.models import CourseComment,Course




def create_course_comment(user_id,data):
    course_id = data.get("course_id")
    content = data.get("content")
    rating = data.get("rating")
    reaction = data.get("reaction")
    
    comment = CourseComment.objects.create(
        user_id=user_id,
        course_id=course_id,
        content=content,
        rating=rating,
        reaction=reaction
    )

    return comment