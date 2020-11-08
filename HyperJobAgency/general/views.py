from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.generic import CreateView
from django.views.generic import ListView, TemplateView

from resume.forms import ResumeCreateForm
from vacancy.forms import VacancyCreateForm


class MenuView(TemplateView):
    template_name = 'menu.html'


class ArticlesListView(ListView):
    template_name = 'articles_list.html'
    page_title = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = self.page_title
        return context


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_staff:
            context['article_type'] = 'vacancy'
            context['form'] = VacancyCreateForm()
        else:
            context['article_type'] = 'resume'
            context['form'] = ResumeCreateForm()

        return context


@method_decorator(login_required, name='dispatch')
class ArticleCreateView(CreateView):
    user_is_staff_condition = None
    success_url = 'home'

    def post(self, request, *args, **kwargs):
        if self.request.user.is_staff == self.user_is_staff_condition:
            return super().post(request, *args, **kwargs)

        return HttpResponse(status=403)

    def form_valid(self, form):
        article = form.save(commit=False)
        article.author = self.request.user
        article.save()
        return redirect(self.success_url)
