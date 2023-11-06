from rest_framework import viewsets
from django.shortcuts import render
from forum.chat import serializers
from models import Message
from serializers import MessageSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from django.http import HttpResponse
from rest_framework import status

# Create your views here.
class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated,]

    def get_queryset(self):
        user_id = self.request.user.id
        if user_id:       
            queryset = Message.objects.filter(sent_to = user_id, seen = False)
            return queryset
        return super().get_queryset()
    
    def perform_create(self, serializer):
        user_id = self.request.user.id
        check_author(serializer.validated_data.get('send_by').id, user_id)
        return super().perform_create(serializer)
    
@api_view(['PUT'])
def mark_as_seen(request):
    user_id = request.user.id
    data = request.data
    receptor_id = data['sent_to']
    serializers = MessageSerializer(data = request.data,many = True)

    if serializer.is_valid():
            serializer.save()
            return HttpResponse(json.dumps({'message': 'Saved'}), content_type='application/json',
                                status=status.HTTP_201_CREATED)
    else:
        return HttpResponse(json.dumps(serializer.errors), content_type='application/json',
                                status=status.HTTP_400_BAD_REQUEST)
    
def check_implied(sender_id, receptor_id, user_id):
    if sender_id != user_id and receptor_id != user_id:
        error_message = {"error":"Only the sender and receptor are able to request a message"}
        raise ValidationError(detail=error_message)
    
def check_author(sender_id, user_id):
    if sender_id != user_id:
        error_message = {"error":"Cant send a message or delete it if you arent the author"}
        raise ValidationError(detail=error_message)

