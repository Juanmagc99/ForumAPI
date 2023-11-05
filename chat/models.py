from django.db import models
from django.contrib.auth.models import User  

class Message(models.Model):
    send_by = models.ForeignKey(User , related_name='messages', 
                              on_delete=models.CASCADE)
    send_to = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    sent_at = models.DateField(auto_now_add=True)
    seen = models.BooleanField(default=False)

    class Meta:
        ordering = ["-sent_at"]