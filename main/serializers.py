from rest_framework import serializers

from .models import Comment, SavedThread, Thread

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class ThreadSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Thread
        fields = '__all__'

class SavedThreadSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedThread
        fields = '__all__'
    