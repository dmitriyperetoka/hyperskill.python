from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class AbstractVacancy(models.Model):
    """Base class for the models of vacancies and other articles
    with the same basic data structure.
    """

    foreign_key_related_name = None
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name=foreign_key_related_name
    )
    description = models.TextField(
        verbose_name='Description', max_length=1024,
        help_text='Fill in the description here.'
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.description[:25]


class Vacancy(AbstractVacancy):
    """Store vacancies in the database."""

    foreign_key_related_name = 'vacancies'
