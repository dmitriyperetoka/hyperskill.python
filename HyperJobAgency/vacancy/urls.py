from django.urls import path
from django.views.generic import RedirectView

from . import views

urlpatterns = [
    path('home/', views.HomeView.as_view(), name='home'),
    path(
        'vacancy/new', views.VacancyCreateView.as_view(), name='create_vacancy'
    ),
    path('vacancy/new/', RedirectView.as_view(url='/vacancy/new')),
    path('vacancies/', views.VacancyListView.as_view(), name='vacancy_list'),
    path('', views.MenuView.as_view(), name='menu'),
]
