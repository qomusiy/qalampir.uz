from django.db import models
from django.contrib.auth.models import User
from habar.models import Habar

# Create your models here.




class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Habar, on_delete=models.CASCADE)
    writing = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}, on {self.post.title}"
    


class CommentLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'comment')  # Ensures a user can like a comment only once

    def __str__(self):
        return f"{self.user.username} likes {self.comment.id}"