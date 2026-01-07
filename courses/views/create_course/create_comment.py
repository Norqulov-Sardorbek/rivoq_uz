from rest_framework import serializers,status
from rest_framework.response import Response
from rest_framework.views import APIView
from courses.services.create_course.create_comments import create_course_comment
from drf_yasg.utils import swagger_auto_schema



class CreateCourseCommentSerializer(serializers.Serializer):
    course_id = serializers.IntegerField()
    content = serializers.CharField()
    rating = serializers.IntegerField()
    reaction = serializers.CharField()
    
    
    
class CreateCourseCommentView(APIView):
    @swagger_auto_schema(
        operation_summary="Create a comment for a course",
        operation_description="Endpoint to create a comment for a specific course.",
        request_body=CreateCourseCommentSerializer,
        responses={201: "Comment created successfully", 400: "Bad Request"},
    )
    def post(self, request):
        serializer = CreateCourseCommentSerializer(data=request.data)
        if serializer.is_valid():
            user_id = request.user.id
            comment = create_course_comment(user_id, serializer.validated_data)
            return Response({"message": "Comment created successfully", "comment_id": comment.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)