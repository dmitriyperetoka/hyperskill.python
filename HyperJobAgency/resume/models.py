from django.contrib.auth.models import User
from django.db import models


class Resume(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='resumes'
    )
    description = models.TextField(max_length=1024)
