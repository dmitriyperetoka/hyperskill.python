from django.urls import path
from django.views.generic import RedirectView

from . import views

urlpatterns = [
    path('resume/new', views.ResumeCreateView.as_view(), name='create_resume'),
    path('resume/new/', RedirectView.as_view(url='/resume/new')),
    path('resumes/', views.ResumeListView.as_view(), name='resume_list'),
]
