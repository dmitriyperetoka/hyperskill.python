from django import forms

from .models import Vacancy


class VacancyCreateForm(forms.ModelForm):
    """Prompt input data for creating vacancies."""

    class Meta:
        model = Vacancy
        fields = ['description']
