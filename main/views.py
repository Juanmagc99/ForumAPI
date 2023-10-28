
from rest_framework.exceptions import ValidationError
from rest_framework import viewsets

from forum.settings import MEDIA_ROOT
from .serializers import CommentSerializer, ThreadSerializer
from .models import Comment, Thread
from rest_framework.permissions import IsAuthenticated
import os

# Create your views here.
class ThreadViewSet(viewsets.ModelViewSet):
    queryset = Thread.objects.all()
    serializer_class = ThreadSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        author_id = self.request.query_params.get('author_id')
        if author_id:
            print("Hola")
            queryset = Thread.objects.filter(author = author_id).order_by('published_date').reverse()
            return queryset
        return super().get_queryset()

    def perform_create(self, serializer):
        user_id = self.request.user.id
        check_author_match(user_id, serializer.validated_data.get('author').id)
        super().perform_create(serializer)
    
    def perform_destroy(self, instance):
        user_id = self.request.user.id
        check_author_match(user_id, instance.author.id)
        return super().perform_destroy(instance)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user_id = self.request.user.id
        check_author_match(user_id, serializer.validated_data.get('author').id)
        super().perform_create(serializer)
    
    def perform_destroy(self, instance):
        user_id = self.request.user.id
        check_author_match(user_id, instance.author.id)
        return super().perform_destroy(instance)


def check_author_match(user_id, author_id):
    if user_id != author_id:
        error_message = {"error": "User making the request is different than the author"}
        raise ValidationError(detail=error_message)
    
