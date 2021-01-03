from django.contrib.auth.models import User
from django.db import models


class AbstractVacancy(models.Model):
    author_field_related_name = None
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name=author_field_related_name
    )
    description = models.TextField(max_length=1024)

    class Meta:
        abstract = True


class Vacancy(AbstractVacancy):
    author_field_related_name = 'vacancies'
