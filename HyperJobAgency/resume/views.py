from .forms import ResumeForm
from .models import Resume
from vacancy.views import VacancyListView, VacancyCreateView


class ResumeListView(VacancyListView):
    """Display list of resumes."""

    page_title = 'Resumes'
    model = Resume


class ResumeCreateView(VacancyCreateView):
    """Create new resumes."""

    form_class = ResumeForm
    is_for_staff = False
