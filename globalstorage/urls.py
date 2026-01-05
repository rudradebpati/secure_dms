from django.urls import path
from . import views

urlpatterns = [
    path(
        "folders/<int:dir_id>/",
        views.DirectoryListCreateView.as_view(),
        name="list_directory",
    ),
    path(
        "open_folder/<int:pk>/",
        views.DirectoryDetailView.as_view(),
        name="create_directory",
    ),
    path(
        "files/",
        views.FileListCreateView.as_view(),
        name="list_files",
    ),
    path(
        "files/<int:pk/download/",
        views.FileDownloadView.as_view(),
        name="file-download",
    ),
]
