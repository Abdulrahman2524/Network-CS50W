from django.contrib.auth.models import AbstractUser
from django.db import models
from . import *

class User(AbstractUser):
    pass

class newPost(models.Model):
    text = models.TextField(null=True)
    date = models.DateTimeField(auto_now_add=True, null=True)
    user = models.ForeignKey(User, related_name="user_post", on_delete=models.CASCADE, null=True)
    def __str__(self):
        return f"{self.user} | {self.text} | {self.date}"
    def serialize(self):
        return {
        "id": self.id,    
        "text": self.text,
        "user": self.user.id,
        "date": self.date,
        }


class UserFollowing(models.Model):

    user_id = models.ForeignKey(User, related_name="following", on_delete=models.CASCADE)
    following_user_id = models.ForeignKey(User, related_name="followers", on_delete=models.CASCADE)

    def serialize(self):
        return {
            "user": self.user_id.id,
            "follower": self.following_user_id.id,
        }
class likePost(models.Model):
    user = models.ForeignKey(User, related_name="user_like", on_delete=models.CASCADE, null=True)
    post = models.ForeignKey(newPost, related_name="post_like", on_delete=models.CASCADE, null=True)
    like = models.BooleanField(null=True, default=False)
    
    def __str__(self):
        return f"{self.user} | {self.post} | {self.like}"

    def serialize(self):
        return {
            "user": self.user.id,
            "post": self.post.id,
            "like": self.like
        }
