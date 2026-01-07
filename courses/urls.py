from django.urls import path
from courses.views.create_course.create_module import CreateModuleView
from courses.views.create_course.create_course import CreateCourseView
from courses.views.create_course.create_lesson import CreateLessonView
from courses.views.create_course.create_comment import CreateCourseCommentView
from courses.views.create_course.create_what_we import CreateWhatWeOfferView,CreateWhoIsThisCourseForView
from courses.views.get_courses.get_courses import GetCoursesView
from courses.views.get_courses.get_course_details import GetCourseDetailView
from courses.views.get_courses.get_modules import GetCourseModulesView
# from courses.views.get_courses.get_lessons import GetCourseLessonsView
from courses.views.get_courses.get_comments import GetCourseCommentsView


urlpatterns = [
    path('create/course/', CreateCourseView.as_view(), name='create_course'),
    path('create/module/', CreateModuleView.as_view(), name='create_module'),
    path('create/lesson/', CreateLessonView.as_view(), name='create_lesson'),
    path('create/comment/', CreateCourseCommentView.as_view(), name='create_course_comment'),
    path('create/what-we-offer/', CreateWhatWeOfferView.as_view(), name='create_what_we_offer'),
    path('create/who-is-this-course-for/', CreateWhoIsThisCourseForView.as_view(), name='create_who_is_this_course_for'),
    # Get endpoints
    path('get-courses/', GetCoursesView.as_view(), name='get_courses'),
    path('get-course-details/', GetCourseDetailView.as_view(), name='get_course_details'),
    path('get-course-modules/', GetCourseModulesView.as_view(), name='get_course_modules'),
    # path('get-course-lessons/', GetCourseLessonsView.as_view(), name='get_course_lessons'),
    path('get-course-comments/', GetCourseCommentsView.as_view(), name='get_course_comments'),
    
]