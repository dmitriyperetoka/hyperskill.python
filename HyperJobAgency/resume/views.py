from .models import Resume
from .forms import ResumeCreateForm
from general.views import ArticlesListView, ArticleCreateView


class ResumesListView(ArticlesListView):
    page_title = 'Resumes'
    model = Resume


class ResumeCreateView(ArticleCreateView):
    form_class = ResumeCreateForm
    user_is_staff_condition = False
