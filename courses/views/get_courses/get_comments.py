from rest_framework import serializers,status
from rest_framework.response import Response
from rest_framework.views import APIView
from courses.services.get_course.get_comments import get_course_comments
from drf_yasg.utils import swagger_auto_schema



class GetCourseCommentsSerializer(serializers.Serializer):
    class CommentSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        user_email = serializers.EmailField()
        rating = serializers.IntegerField()
        reaction = serializers.CharField()
        comment = serializers.CharField()
        created_at = serializers.DateTimeField()
    course_id = serializers.IntegerField(required=True, help_text="ID of the course to get comments for")
    comments = CommentSerializer(many=True)
    
    
class GetCourseCommentsView(APIView):
    @swagger_auto_schema(
        operation_description="Retrieve comments for a specific course.",
        responses={200: GetCourseCommentsSerializer()},
        tags=["Courses"]
    )
    def get(self, request, course_id):
        """
        Retrieve comments for a specific course.
        """
        comments_data = get_course_comments(course_id)
        serializer = GetCourseCommentsSerializer(comments_data)
        return Response(serializer.data, status=status.HTTP_200_OK)
    