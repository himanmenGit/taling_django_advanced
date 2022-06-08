from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )
    nickname = models.CharField(null=False, max_length=20)
    profile_image = models.ImageField(upload_to="uploads/%Y/%m/%d/", null=True)
