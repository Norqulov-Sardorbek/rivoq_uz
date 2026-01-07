from rest_framework import serializers,status
from rest_framework.response import Response
from rest_framework.views import APIView
from courses.services.create_course.create_module import create_module
from drf_yasg.utils import swagger_auto_schema



class CreateModuleSerializer(serializers.Serializer):
    course_id = serializers.IntegerField()
    title = serializers.CharField(max_length=255)
    order = serializers.IntegerField()
    description = serializers.CharField()
    
class CreateModuleView(APIView):
    @swagger_auto_schema(
        operation_summary="Create a new module",
        operation_description="Endpoint to create a new module within a course.",
        request_body=CreateModuleSerializer,
        responses={201: "Module created successfully", 400: "Bad Request"}
    )
    def post(self, request):
        serializer = CreateModuleSerializer(data=request.data)
        if serializer.is_valid():
            module = create_module(serializer.validated_data)
            return Response({"message": "Module created successfully", "module_id": module.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


