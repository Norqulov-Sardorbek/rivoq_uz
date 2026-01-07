from rest_framework import serializers,status
from rest_framework.response import Response
from rest_framework.views import APIView
from courses.services.get_course.get_courses import get_courses
from drf_yasg.utils import swagger_auto_schema





class GetCoursesSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    image = serializers.URLField(allow_null=True)
    
    
class GetCoursesView(APIView):
    @swagger_auto_schema(
        operation_description="Get list of started courses",
        responses={200: GetCoursesSerializer(many=True)}
    )
    def get(self, request):
        courses_data = get_courses()
        serializer = GetCoursesSerializer(courses_data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)