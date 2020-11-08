from django import forms

from .models import Vacancy


class VacancyCreateForm(forms.ModelForm):
    class Meta:
        model = Vacancy
        fields = ('description',)
