import json
from django.http import HttpResponse
from requests import Response, delete
from rest_framework.exceptions import ValidationError
from rest_framework import viewsets
from rest_framework.views import APIView
from forum.settings import MEDIA_ROOT
from .serializers import CommentSerializer, SavedThreadSerializer, ThreadSerializer
from .models import Comment, SavedThread, Thread
from rest_framework.permissions import IsAuthenticated
from rest_framework import status


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

class SavedThreadView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_id = request.user.id
        threads = [t.thread for t in SavedThread.objects.filter(user = user_id).all()]
        serializer = ThreadSerializer(threads, many = True)
        return HttpResponse(json.dumps(serializer.data), content_type='application/json'
                            , status=status.HTTP_200_OK)

    def post(self, request):
        user_id = request.user.id
        data = request.data
        data['user'] = user_id
        serializer = SavedThreadSerializer(data=data)
    
        if serializer.is_valid():
            serializer.save()
            return HttpResponse(json.dumps({'message': 'Saved'}), content_type='application/json',
                                status=status.HTTP_201_CREATED)
        else:
            return HttpResponse(json.dumps(serializer.errors), content_type='application/json',
                                 status=status.HTTP_400_BAD_REQUEST)
    


def check_author_match(user_id, author_id):
    if user_id != author_id:
        error_message = {"error": "User making the request is different than the author"}
        raise ValidationError(detail=error_message)
    
