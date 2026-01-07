from rest_framework import serializers,status
from rest_framework.response import Response
from rest_framework.views import APIView
from courses.services.create_course.create_what_we_offer import create_what_we_offer,create_who_is_this_course_for
from drf_yasg.utils import swagger_auto_schema

class CreateWhatWeOfferSerializer(serializers.Serializer):
    course_id = serializers.IntegerField()
    title = serializers.CharField(max_length=200)
    description = serializers.CharField(required=False, allow_blank=True)

class CreateWhoIsThisCourseForSerializer(serializers.Serializer):
    course_id = serializers.IntegerField()
    title = serializers.CharField(max_length=255)

class CreateWhatWeOfferView(APIView):
    @swagger_auto_schema(
        operation_summary="Create What We Offer entry",
        operation_description="Endpoint to create a 'What We Offer' entry for a course.",
        request_body=CreateWhatWeOfferSerializer,
        responses={201: "What We Offer created successfully", 400: "Bad Request"}
    )
    def post(self, request):
        serializer = CreateWhatWeOfferSerializer(data=request.data)
        if serializer.is_valid():
            what_we_offer = create_what_we_offer(serializer.validated_data)
            return Response({"message": "What We Offer created successfully", "id": what_we_offer.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CreateWhoIsThisCourseForView(APIView):
    @swagger_auto_schema(
        operation_summary="Create Who Is This Course For entry",
        operation_description="Endpoint to create a 'Who Is This Course For' entry for a course.",
        request_body=CreateWhoIsThisCourseForSerializer,
        responses={201: "Entry created successfully", 400: "Bad Request"}
    )
    def post(self, request):
        serializer = CreateWhoIsThisCourseForSerializer(data=request.data)
        if serializer.is_valid():
            who_is_for = create_who_is_this_course_for(serializer.validated_data)
            return Response({"message": "Entry created successfully", "id": who_is_for.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)