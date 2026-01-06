from django.db import models
from core.models.basemodel import SafeBaseModel
from courses.models import Course
from users.models import CustomUser
# Create your models here.





class Interview(SafeBaseModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE , related_name="interview")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE , related_name="interview")
    scheduled_at = models.DateTimeField(null=True, blank=True)
    feedback = models.TextField(null=True, blank=True)
    is_passed = models.BooleanField(default=False)
    
    def __str__(self):
        return f'Interview for {self.user.full_name} on {self.scheduled_at}'
    
    
class InterviewVideo(SafeBaseModel):
    interview = models.ForeignKey(Interview, on_delete=models.CASCADE, related_name='videos')
    video_url = models.URLField()
    description = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return f'Video for Interview  {self.interview.user.full_name}'