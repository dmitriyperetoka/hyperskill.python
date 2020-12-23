from django.contrib.auth.views import LogoutView
from django.urls import path
from django.views.generic import RedirectView

from agency import views

urlpatterns = [
    path('resume/new', views.ResumeCreateView.as_view(), name='create_resume'),
    path('resumes/', views.ResumeListView.as_view(), name='resumes_list'),
    path(
        'vacancy/new', views.VacancyCreateView.as_view(), name='create_vacancy'
    ),
    path(
        'vacancies/', views.VacancyListView.as_view(), name='vacancies_list'
    ),
    path('signup', views.TheSignupView.as_view(), name='signup'),
    path('login', views.TheLoginView.as_view(), name='login'),
    path('home/', views.HomeView.as_view(), name='home'),
    path('', views.MenuView.as_view(), name='menu'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', RedirectView.as_view(url='/signup')),
    path('login/', RedirectView.as_view(url='/login')),
    path('resume/new/', RedirectView.as_view(url='/resume/new')),
    path('vacancy/new/', RedirectView.as_view(url='/vacancy/new')),
]
