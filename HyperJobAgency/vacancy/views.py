from .forms import VacancyCreateForm
from .models import Vacancy
from general.views import ArticleCreateView, ArticlesListView


class VacanciesListView(ArticlesListView):
    page_title = 'Vacancies'
    model = Vacancy


class VacancyCreateView(ArticleCreateView):
    form_class = VacancyCreateForm
    user_is_staff_condition = True
