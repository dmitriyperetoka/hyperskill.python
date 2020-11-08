from django.contrib.auth.views import LogoutView
from django.urls import path
from django.views.generic import RedirectView

from . import views as general_views
from resume import views as resume_views
from vacancy import views as vacancy_views

urlpatterns = [
    path(
        'resume/new',
        resume_views.ResumeCreateView.as_view(),
        name='create_resume'
    ),
    path(
        'resumes/',
        resume_views.ResumesListView.as_view(),
        name='resumes_list'
    ),
    path(
        'vacancy/new',
        vacancy_views.VacancyCreateView.as_view(),
        name='create_vacancy'
    ),
    path(
        'vacancies/',
        vacancy_views.VacanciesListView.as_view(),
        name='vacancies_list'
    ),
    path('signup', general_views.TheSignupView.as_view(), name='signup'),
    path('login', general_views.TheLoginView.as_view(), name='login'),
    path('home/', general_views.HomeView.as_view(), name='home'),
    path('', general_views.MenuView.as_view(), name='menu'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', RedirectView.as_view(url='/signup')),
    path('login/', RedirectView.as_view(url='/login')),
    path('resume/new/', RedirectView.as_view(url='/resume/new')),
    path('vacancy/new/', RedirectView.as_view(url='/vacancy/new')),
]
