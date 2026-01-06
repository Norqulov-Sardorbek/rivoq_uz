from rest_framework.views import APIView
from rest_framework.response import Response






class Hug(APIView):
    """
    A simple API view that returns a hug message.
    """

    def get(self, request, *args, **kwargs):
        return Response({"message": "Here's a big hug for you!"})