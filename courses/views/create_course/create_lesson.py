from rest_framework import serializers,status
from rest_framework.response import Response
from rest_framework.views import APIView
from courses.services.create_course.create_lesson import create_lesson
from drf_yasg.utils import swagger_auto_schema


class CreateLessonSerializer(serializers.Serializer):
    module_id = serializers.IntegerField()
    title = serializers.CharField(max_length=255)
    order = serializers.IntegerField()
    video_url = serializers.URLField()
    duration = serializers.IntegerField()
    description = serializers.CharField()
    code_source = serializers.URLField()
    
class CreateLessonView(APIView):
    @swagger_auto_schema(
        operation_summary="Create a new lesson",
        operation_description="Endpoint to create a new lesson within a module.",
        request_body=CreateLessonSerializer,
        responses={201: "Lesson created successfully", 400: "Bad Request"}
    )
    def post(self, request):
        serializer = CreateLessonSerializer(data=request.data)
        if serializer.is_valid():
            lesson = create_lesson(serializer.validated_data)
            return Response({"message": "Lesson created successfully", "lesson_id": lesson.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

