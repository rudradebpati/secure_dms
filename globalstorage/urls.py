from django.urls import path
from . import views

urlpatterns = [
    path(
        "folders/<int:dir_id>/",
        views.DirectoryListCreateView.as_view(),
        name="list_directory",
    ),  # POST for creation of subfolder
    path(
        "folders/",
        views.DirectoryListCreateView.as_view(),
        name="list_directory",
    ),  # POST for empty folder on surface level
    path(
        "folders/",
        views.DirectoryListCreateView.as_view(),
        name="list_directory",
    ),  # GET for all folders list
    path(
        "open_folder/<int:pk>/",
        views.DirectoryDetailView.as_view(),
        name="create_directory",
    ),  # GET
    path(
        "files/",
        views.FileListCreateView.as_view(),
        name="list_files",
    ),  # GET, POST
    path(
        "files/<int:pk>/download/",
        views.FileDownloadView.as_view(),
        name="file-download",
    ),  # GET
]
