from django.contrib import admin

from .models import Comment, SavedThread, Thread

# Register your models here.
admin.site.register([Thread, Comment, SavedThread])