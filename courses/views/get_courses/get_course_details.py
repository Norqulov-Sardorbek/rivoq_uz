from rest_framework import serializers,status
from rest_framework.response import Response
from rest_framework.views import APIView
from courses.services.get_course.get_course_detail import get_course_detail
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class GetCourseDetailSerializer(serializers.Serializer):
    class WhatWeOfferSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        title = serializers.CharField()
        description = serializers.CharField(allow_null=True)
    class WhoIsThisCourseForSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        title = serializers.CharField()
    id = serializers.IntegerField()
    title = serializers.CharField()
    description = serializers.CharField()
    teachers = serializers.CharField()
    image = serializers.URLField(allow_null=True)
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    is_free = serializers.BooleanField()
    is_started = serializers.BooleanField()
    students_enrolled = serializers.IntegerField()
    created_at = serializers.DateTimeField()
    lessons_count = serializers.IntegerField()
    average_rating = serializers.FloatField()
    duration = serializers.IntegerField()
    what_we_offer = WhatWeOfferSerializer(many=True)
    who_is_for = WhoIsThisCourseForSerializer(many=True)


class GetCourseDetailView(APIView):
    @swagger_auto_schema(
        operation_description="Get details of a specific course by ID",
        manual_parameters=[
            openapi.Parameter(
                'course_id',
                openapi.IN_QUERY,
                description="ID of the course to retrieve details for",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        responses={200: GetCourseDetailSerializer()}
    )
    def get(self, request):
        course_id = request.query_params.get('course_id')
        course_data = get_course_detail(course_id)
        serializer = GetCourseDetailSerializer(course_data)
        return Response(serializer.data, status=status.HTTP_200_OK)