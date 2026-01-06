from django.urls import path
from courses.views.just_apii import Hug

urlpatterns = [
    path('hug/', Hug.as_view(), name='course_list'),
]