from django.db import models
from django.contrib.auth.models import User    
import os
import uuid

def subfolder_manage(instance, filename):
    extension = os.path.splitext(filename)[1]
    filename = f'{uuid.uuid4().hex[:8]}_{instance.published_date}.{extension}'
    return f'thread_pictures/{instance.author.id}/{filename}'

# Create your models here.
class Thread(models.Model):
    author =models.ForeignKey(User , related_name='threads', 
                              on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    body = models.TextField()
    published_date = models.DateField(auto_now_add=True)
    picture = models.ImageField(upload_to= subfolder_manage
                                , null=True, blank=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    thread = models.ForeignKey(Thread, related_name='comments', 
                               on_delete=models.CASCADE)
    author = models.ForeignKey(User , related_name='comments', 
                              on_delete=models.CASCADE)
    body = models.TextField()
    published_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return "Comment in " + self.thread.title
    
class SavedThread(models.Model):
    user = models.ForeignKey(User, related_name='saved',
                             on_delete=models.CASCADE)
    thread = models.ForeignKey(Thread, related_name='saved',
                             on_delete=models.CASCADE)