from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Create your views here.

class ScheduleListAPIView(APIView):
    def get(self, request):
        return 111
        
        
        
class ScheduleDetailAPIView(APIView):
    def post(self, request):
        return 222