from typing import Dict, Union

from django.contrib.auth.decorators import login_required
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from django.http.response import (
    HttpResponse, HttpResponseForbidden, HttpResponseNotAllowed,
    HttpResponseRedirect,
)
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.generic import CreateView
from django.views.generic import ListView, TemplateView

from .forms import VacancyForm
from .models import Vacancy
from resume.forms import ResumeForm


class MenuView(TemplateView):
    """Display menu page."""

    template_name = 'menu.html'

    def get_context_data(self):
        greeting_message = 'Welcome to HyperJob!'
        menu = ['login', 'signup', 'vacancies', 'resumes', 'home', 'logout']

        return {'greeting_message': greeting_message, 'menu': menu}


@method_decorator(login_required, name='get')
class HomeView(TemplateView):
    """Display the profile page of the user."""

    template_name = 'home.html'

    def get_context_data(self) -> (
            Dict[str, Union[str, ResumeForm, VacancyForm]]
    ):
        if self.request.user.is_staff:
            object_type = 'vacancy'
            form = VacancyForm()
        else:
            object_type = 'resume'
            form = ResumeForm()

        return {'object_type': object_type, 'form': form}


@method_decorator(login_required, name='post')
class VacancyCreateView(CreateView):
    """Create new vacancies."""

    form_class = VacancyForm
    success_url = 'home'
    is_for_staff = True

    def dispatch(self, request: HttpRequest) -> (
            Union[HttpResponse, HttpResponseForbidden, HttpResponseNotAllowed]
    ):
        if request.method != 'POST':
            return HttpResponseNotAllowed(['POST'])

        return super().dispatch(request)

    def post(self, request: HttpRequest) -> (
            Union[HttpResponse, HttpResponseForbidden]
    ):
        if self.request.user.is_staff == self.is_for_staff:
            return super().post(request)

        return HttpResponseForbidden()

    def form_valid(self, form: Union[ResumeForm, VacancyForm]) -> (
            HttpResponseRedirect
    ):
        article = form.save(commit=False)
        article.author = self.request.user
        article.save()
        return redirect(self.success_url)


class VacancyListView(ListView):
    """Display list of vacancies."""

    template_name = 'vacancy_list.html'
    page_title = 'Vacancies'
    model = Vacancy

    def get_context_data(self) -> Dict[str, Union[str, QuerySet]]:
        object_list = super().get_context_data().get('object_list')
        return {'object_list': object_list, 'page_title': self.page_title}
