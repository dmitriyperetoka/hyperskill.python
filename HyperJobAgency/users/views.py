from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView


class SignupView(CreateView):
    """Create new user accounts."""

    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


class TheLoginView(LoginView):
    """Authenticate users."""

    form_class = AuthenticationForm
    redirect_authenticated_user = True
    template_name = 'login.html'
