from rest_framework import serializers,status
from rest_framework.response import Response
from rest_framework.views import APIView
from courses.services.create_course.create_course import create_course
from drf_yasg.utils import swagger_auto_schema



class CreateCourseSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    image = serializers.ImageField()
    is_started = serializers.BooleanField(default=False)
    is_free = serializers.BooleanField(default=True)
    description = serializers.CharField(allow_blank=True, required=False)
    price = serializers.FloatField(default=0.0)
    teachers = serializers.CharField(allow_blank=True, required=False)
    
class CreateCourseView(APIView):
    @swagger_auto_schema(operation_summary="Create a new course", 
                         operation_description="Endpoint to create a new course with the provided details.",
                         request_body=CreateCourseSerializer,
                         responses={201: "Course created successfully", 400: "Bad Request"},
                         )
    def post(self, request):
        serializer = CreateCourseSerializer(data=request.data)
        if serializer.is_valid():
            course = create_course(serializer.validated_data, request.FILES.get('image'))
            return Response({'message': 'Course created successfully', 'course_id': course.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)