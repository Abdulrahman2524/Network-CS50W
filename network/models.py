from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class newPost(models.Model):
    text = models.TextField(null=True)
    date = models.DateTimeField(auto_now_add=True, null=True)
    user = models.ForeignKey(User, related_name="user_post", on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.user} | {self.text} | {self.date}"

class UserFollowing(models.Model):

    user_id = models.ForeignKey(User, related_name="following", on_delete=models.CASCADE)
    following_user_id = models.ForeignKey(User, related_name="followers", on_delete=models.CASCADE)

    def serialize(self):
        return {
            "user": self.user_id.id,
            "follower": self.following_user_id.id,
        }
