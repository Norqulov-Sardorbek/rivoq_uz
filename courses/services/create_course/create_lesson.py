from courses.models import Lesson





def create_lesson(data):
    module_id = data.get("module_id")
    title = data.get("title")
    order = data.get("order")
    video_url = data.get("video_url")
    duration = data.get("duration")
    description = data.get("description")
    code_source = data.get("code_source")
    
    lesson = Lesson.objects.create(
        module_id=module_id,
        title=title,
        order=order,
        video_url=video_url,
        duration=duration,
        description=description,
        code_source=code_source
    )

    return lesson   
    