from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
# Create your views here.


class AppointMentAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, patient_id):
        
        return Response("zpzpzpzpzpzpzpzp")
