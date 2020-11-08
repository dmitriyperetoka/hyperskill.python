from django import forms

from .models import Resume


class ResumeCreateForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ('description',)
