from django.contrib.auth.views import LogoutView
from django.urls import path
from django.views.generic import RedirectView

from . import views

urlpatterns = [
    path('signup', views.SignupView.as_view(), name='signup'),
    path('signup/', RedirectView.as_view(url='/signup')),
    path('login', views.TheLoginView.as_view(), name='login'),
    path('login/', RedirectView.as_view(url='/login')),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('home/', views.HomeView.as_view(), name='home'),
    path(
        'vacancy/new', views.VacancyCreateView.as_view(), name='create_vacancy'
    ),
    path('vacancy/new/', RedirectView.as_view(url='/vacancy/new')),
    path('vacancies/', views.VacancyListView.as_view(), name='vacancies_list'),
    path('', views.MenuView.as_view(), name='menu'),
]
