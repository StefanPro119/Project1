from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:title>", views.entry, name="entry"),
    path('search/', views.search, name="search"),
    path('create/', views.create, name="create"),
    path("<str:title>/edit/", views.edit, name="edit_page"),
    path("<str:title>/submit_edit/", views.submit_edit, name="submit_edit")
]