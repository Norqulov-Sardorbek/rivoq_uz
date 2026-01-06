from django.db import models
from core.models.basemodel import SafeBaseModel
from courses.models import Course
from users.models import CustomUser
# Create your models here.



class Test(SafeBaseModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='tests')
    title = models.CharField(max_length=200)
    deadline_time = models.IntegerField(help_text="Vaqtni minutlarda kiriting")
    description = models.TextField(null=True, blank=True)
    
    
    def __str__(self):
        return f'{self.title} - {self.course.title}'

class Question(SafeBaseModel):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='questions')
    question = models.TextField()
    point = models.FloatField( default=0.9)

    answer_a = models.TextField(blank=True, null=True)
    answer_b = models.TextField(blank=True, null=True)
    answer_c = models.TextField(blank=True, null=True)
    answer_d = models.TextField(blank=True, null=True)
    
    CORRECT_OPTION = (
    ("a", "A"),
    ("b", "B"),
    ("c", "C"),
    ("d", "D"),
    )
    correct_answer = models.CharField(max_length=1, choices=CORRECT_OPTION, blank=True, null=True)
    
    def __str__(self):
        return f'Question for {self.test.title}'
    
    
    

    
class UserTestResult(SafeBaseModel):
    user=models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='test_results')
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    total_questions = models.IntegerField(default=0)
    correct_answers = models.IntegerField(default=0)
    wrong_answers = models.IntegerField(default=0)
    unanswered = models.IntegerField(default=0)
    score = models.FloatField(default=0.0)
    total_score = models.FloatField(default=0.0)
    
    class Meta:
        verbose_name = 'Foydalanuvchi Test Natijasi'
        verbose_name_plural = 'Foydalanuvchi Test Natijalari'

    def __str__(self):
        return f"User {self.user.full_name} - Test {self.test.title} - Score {self.score}"
    
    
class UserAnswer(SafeBaseModel):
    user_test = models.ForeignKey(UserTestResult, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='user_answers')
    answer = models.CharField(max_length=255, blank=True, null=True)
    ANSWER_STATUS = (
    ("correct", "Correct"),
    ("wrong", "Wrong"),
    ("unanswered", "Unanswered"),
)
    status = models.CharField(max_length=12, choices=ANSWER_STATUS, default="unanswered")
    
    class Meta:
        verbose_name = 'Foydalanuvchi Javobi'
        verbose_name_plural = 'Foydalanuvchi Javoblari'
    def __str__(self):
        return f"User {self.user_test.user.full_name} - Question {self.question.id} - Answer {self.answer}"