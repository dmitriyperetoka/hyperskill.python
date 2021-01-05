from django.urls import path

from . import views

urlpatterns = [
    path('news/<int:link>/', views.article_page, name='article_page'),
    path('news/create/', views.create_article, name='create_article'),
    path('news/', views.main_page, name='main_page'),
    path('', views.index, name='index'),
]
