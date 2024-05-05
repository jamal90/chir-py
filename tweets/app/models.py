from django.db import models

from django.contrib.auth.models import User, AbstractUser


class Tweet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"id = {self.id}, user_id = {self.user.id} content = {self.content}"


class Following(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')

    # in case the target user deleted his account, we can still retain the relationship to show the user does not exist
    following = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='following')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"id = {self.id}, user_id = {self.user.id} follower_id = {self.following.id}"
