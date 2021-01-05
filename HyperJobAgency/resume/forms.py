from .models import Resume
from vacancy.forms import VacancyCreateForm


class ResumeCreateForm(VacancyCreateForm):
    """Prompt input data for creating resumes."""

    class Meta(VacancyCreateForm.Meta):
        model = Resume
