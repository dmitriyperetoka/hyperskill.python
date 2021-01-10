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
]
