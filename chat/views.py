from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from .models import Message
from .serializers import MessageSerializer
from rest_framework.permissions import IsAuthenticated


class MessageListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        messages = Message.objects.filter(
            sender=request.user) | Message.objects.filter(receiver=request.user)
        messages = messages.order_by('timestamp')
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(sender=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MessageDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            message = Message.objects.get(pk=pk)
        except Message.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if message.sender != request.user and message.receiver != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)

        serializer = MessageSerializer(message)
        return Response(serializer.data)
