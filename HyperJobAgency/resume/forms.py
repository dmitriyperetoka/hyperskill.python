from .models import Resume
from vacancy.forms import VacancyCreateForm


class ResumeCreateForm(VacancyCreateForm):
    class Meta(VacancyCreateForm.Meta):
        model = Resume
