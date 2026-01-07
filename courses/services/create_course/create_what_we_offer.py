from courses.models import WhoIsThisCourseFor,WhatWeOffer


def create_what_we_offer(data):
    course_id = data.get('course_id')
    title = data.get('title')
    description = data.get('description','')
    
    what_we_offer = WhatWeOffer.objects.create(
        course_id=course_id,
        title=title,
        description=description
    )
    return what_we_offer

def create_who_is_this_course_for(data):
    course_id = data.get('course_id')
    title = data.get('title')
    
    who_is_for = WhoIsThisCourseFor.objects.create(
        course_id=course_id,
        title=title
    )
    return who_is_for