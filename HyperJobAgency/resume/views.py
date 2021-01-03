from .forms import ResumeCreateForm
from .models import Resume
from vacancy.views import VacancyListView, VacancyCreateView


class ResumeListView(VacancyListView):
    page_title = 'Resumes'
    model = Resume


class ResumeCreateView(VacancyCreateView):
    form_class = ResumeCreateForm
    is_for_staff = False
