from .forms import ResumeCreateForm
from .models import Resume
from vacancy.views import VacancyListView, VacancyCreateView


class ResumeListView(VacancyListView):
    """Display list of resumes."""

    page_title = 'Resumes'
    model = Resume


class ResumeCreateView(VacancyCreateView):
    """Create new resumes."""

    form_class = ResumeCreateForm
    is_for_staff = False
