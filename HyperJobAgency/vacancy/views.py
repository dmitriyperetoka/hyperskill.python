from typing import Any, Dict

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.views import LoginView
from django.http.response import HttpResponse, HttpResponseRedirect
from django.http.request import HttpRequest
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.generic import CreateView
from django.views.generic import ListView, TemplateView

from .forms import VacancyCreateForm
from .models import Vacancy
from resume.forms import ResumeCreateForm


class MenuView(TemplateView):
    template_name = 'menu.html'


class TheSignupView(CreateView):
    form_class = UserCreationForm
    success_url = 'login'
    template_name = 'signup.html'


class TheLoginView(LoginView):
    form_class = AuthenticationForm
    redirect_authenticated_user = True
    template_name = 'login.html'


@method_decorator(login_required, name='dispatch')
class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs: Dict[str, Any]) -> Dict[str, str]:
        context = super().get_context_data(**kwargs)

        if self.request.user.is_staff:
            context['article_type'] = 'vacancy'
            context['form'] = VacancyCreateForm()
        else:
            context['article_type'] = 'resume'
            context['form'] = ResumeCreateForm()

        return context


class VacancyListView(ListView):
    template_name = 'articles_list.html'
    page_title = 'Vacancies'
    model = Vacancy

    def get_context_data(self, **kwargs: Dict[str, Any]) -> Dict[str, str]:
        context = super().get_context_data(**kwargs)
        context['page_title'] = self.page_title
        return context


@method_decorator(login_required, name='dispatch')
class VacancyCreateView(CreateView):
    form_class = VacancyCreateForm
    success_url = 'home'
    is_for_staff = True

    def post(
            self,
            request: HttpRequest,
            **kwargs: Dict[str, str]
    ) -> HttpResponse:
        if self.request.user.is_staff == self.is_for_staff:
            return super().post(request, **kwargs)

        return HttpResponse(status=403)

    def form_valid(self, form: VacancyCreateForm) -> HttpResponseRedirect:
        article = form.save(commit=False)
        article.author = self.request.user
        article.save()
        return redirect(self.success_url)
