from rest_framework import viewsets
from django.shortcuts import render
from models import Message
from serializers import MessageSerializer
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated,]

    def get_queryset(self):
        user_id = self.request.user.id
        if user_id:       
            queryset = Message.objects.filter(sent_to = user_id)
            return queryset
        return super().get_queryset()
    
    def perform_create(self, serializer):
        user_id = self.request.user.id
        check_author(serializer.validated_data.get('send_by').id, user_id)
        return super().perform_create(serializer)
    
def check_implied(sender_id, receptor_id, user_id):
    if sender_id != user_id and receptor_id != user_id:
        error_message = {"error":"Only the sender and receptor are able to request a message"}

def check_author(sender_id, user_id):
    if sender_id != user_id:
        error_message = {"error":"Cant send a message or delete it if you arent the author"}