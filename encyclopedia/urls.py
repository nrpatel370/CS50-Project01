from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.title, name="title"),
    path("search", views.search, name="query"),
    path("new_page", views.new_page, name="newpage"),
    path("wiki/<str:title>/edit", views.edit, name="edit"),
    path("random", views.random_page, name="random")
]
