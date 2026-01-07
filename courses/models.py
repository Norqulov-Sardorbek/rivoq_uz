from django.db import models
from users.models import CustomUser
from core.models.basemodel import SafeBaseModel
# Create your models here.



class Course(SafeBaseModel):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='course_images/')
    is_started = models.BooleanField(default=False)
    is_free = models.BooleanField(default=True)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    teachers = models.CharField(max_length=255)
    
    @property
    def average_rating(self):
        feedbacks = self.feedbacks.all()
        if feedbacks.exists():
            return feedbacks.aggregate(models.Avg('rating'))['rating__avg']
        return 0
    
    @property
    def total_duration(self):
        lessons = Lesson.objects.filter(module__course=self)
        return lessons.aggregate(total_duration=models.Sum('duration'))['total_duration'] or 0
    
    @property
    def lessons_count(self):
        return Lesson.objects.filter(module__course=self).count()
    
    def __str__(self):
        return self.title
    


class Module(SafeBaseModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    order = models.PositiveIntegerField()
    
    @property
    def lessons_count(self):
        return self.lessons.count()
    
    @property
    def total_duration(self):
        return self.lessons.aggregate(total_duration=models.Sum('duration'))['total_duration'] or 0
    
    def __str__(self):
        return f'{self.title} - {self.course.title}'


class Lesson(SafeBaseModel):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    order = models.PositiveIntegerField()
    video_url = models.URLField()
    duration = models.PositiveIntegerField(help_text="Duration in minutes")
    description = models.TextField(null=True, blank=True)
    code_source = models.URLField(null=True, blank=True)
    
    
    def __str__(self):
        return f'{self.title} - {self.module.title}'



class CourseComment(SafeBaseModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='feedbacks')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='course_feedbacks')
    rating = models.PositiveIntegerField()
    reaction = models.CharField(max_length=100)
    comment = models.TextField(null=True, blank=True)
    
    
    
    
    def __str__(self):
        return f'Feedback by {self.user.email} for {self.course.title}'
    
class WhatWeOffer(SafeBaseModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='what_we_offer')
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    
    
    def __str__(self):
        return f'What We Offer: {self.title} for {self.course.title}'

class WhoIsThisCourseFor(SafeBaseModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='who_is_for')
    title = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.title} ({self.course.title})'
    
    
class Note(SafeBaseModel):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="notes")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='notes')
    note = models.TextField()   
    
    def __str__(self):
        return f'Note by {self.user.email} for {self.lesson.title}'
    
    
class CourseStudent(SafeBaseModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='students')
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='enrolled_courses')
    in_lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, null=True, blank=True, related_name='current_students')
    
    
    def __str__(self):
        return f'{self.student.email} enrolled in {self.course.title}'