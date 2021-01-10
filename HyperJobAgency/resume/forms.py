from django import forms

from .models import Resume


class ResumeForm(forms.ModelForm):
    """Prompt input data for creating resumes."""

    class Meta:
        model = Resume
        fields = ['description']
