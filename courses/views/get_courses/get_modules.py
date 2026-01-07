from rest_framework import serializers,status
from rest_framework.response import Response
from rest_framework.views import APIView
from courses.services.get_course.get_modules import get_course_modules
from drf_yasg.utils import swagger_auto_schema



class CourseModuleLessonSerializer(serializers.Serializer):
    class ModuleSerializer(serializers.Serializer):
        class LessonSerializer(serializers.Serializer):
            id = serializers.IntegerField()
            title = serializers.CharField()
            order = serializers.IntegerField()
            video_url = serializers.URLField()
            duration = serializers.IntegerField()
            description = serializers.CharField()
            code_source = serializers.URLField()
        id = serializers.IntegerField()
        title = serializers.CharField()
        description = serializers.CharField()
        lessons_count = serializers.IntegerField()
        total_duration = serializers.IntegerField()
        lessons = LessonSerializer(many=True)
    course_id = serializers.IntegerField()
    course_title = serializers.CharField()
    module_count = serializers.IntegerField()
    lesson_count = serializers.IntegerField()
    course_duration = serializers.IntegerField()
    modules = ModuleSerializer(many=True)
    
class GetCourseModulesView(APIView):
    @swagger_auto_schema(
        responses={
            200: CourseModuleLessonSerializer,
            404: 'Course not found'
        }
    )
    def get(self, request, course_id):
        """
        Retrieve modules and lessons for a specific course.
        """
        course_modules_data = get_course_modules(course_id)
        serializer = CourseModuleLessonSerializer(course_modules_data)
        return Response(serializer.data, status=status.HTTP_200_OK)
    