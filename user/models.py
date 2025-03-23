from django.db import models
from django.contrib.auth.models import User
from habar.models import Habar

# Create your models here.




class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Habar, on_delete=models.CASCADE)
    writing = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    like = models.PositiveIntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}, on {self.post.title}"
