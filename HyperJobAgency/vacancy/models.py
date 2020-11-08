from django.contrib.auth.models import User
from django.db import models


class Vacancy(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='vacancies'
    )
    description = models.TextField(max_length=1024)
