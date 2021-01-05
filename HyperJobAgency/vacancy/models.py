from django.contrib.auth.models import User
from django.db import models


class AbstractVacancy(models.Model):
    """Base class for the models of vacancies and other articles
    with the same basic data structure.
    """

    foreign_key_related_name = None
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name=foreign_key_related_name
    )
    description = models.TextField(max_length=1024)

    class Meta:
        abstract = True


class Vacancy(AbstractVacancy):
    """Store vacancies in the database."""

    foreign_key_related_name = 'vacancies'
