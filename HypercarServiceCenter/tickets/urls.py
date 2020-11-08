from django.urls import path
from django.views.generic import RedirectView

from . import views

urlpatterns = [
    path('welcome/', views.WelcomeView.as_view(), name='welcome'),
    path('menu/', views.MenuView.as_view(), name='menu'),
    path(
        'get_ticket/<str:service>/',
        views.GetTicketView.as_view(),
        name='get_ticket'
    ),
    path('processing', views.ProcessingView.as_view(), name='processing'),
    path('processing/', RedirectView.as_view(url='/processing')),
    path('next/', views.NextView.as_view(), name='next'),
]
