from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("save-keyword/", views.save_keyword, name="save_keyword"),
    path("delete/<int:keyword_id>/", views.delete_keyword, name="delete_keyword"),
]
