from courses.models import Course,Module,Lesson




def create_module(data):
    course_id = data.get('course_id')
    title = data.get('title')
    description = data.get('description','')
    order = data.get('order', 0)
    
    module = Module.objects.create(
        course_id=course_id,
        title=title,
        description=description,
        order=order
    )
    return module 