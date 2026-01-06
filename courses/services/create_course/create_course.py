from courses.models import Course



def create_course(data,image):
    title = data.get('title')
    image = data.get('image')
    is_started = data.get('is_started', False)
    is_free = data.get('is_free', True)
    description = data.get('description', '')
    price = data.get('price', 0.0)
    teachers = data.get('teachers', '')
    
    course = Course.objects.create(
        title=title,
        image=image,
        is_started=is_started,
        is_free=is_free,
        description=description,
        price=price,
        teachers=teachers
    )
    return course 