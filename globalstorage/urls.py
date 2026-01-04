from django.urls import path
from . import views

urlpatterns = [
    path("folders/<int:dir_id>/",views.DirectoryListCreateView.as_view(),name="create_directory"),
    path("open_folder/<int:parent_id>/",views.DirectoryListCreateView.as_view(),name="create_directory"),
]
