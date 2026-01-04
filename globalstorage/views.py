from django.http import FileResponse
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from rest_framework import generics
from .access_permissions import IsOwner
from rest_framework.permissions import IsAuthenticated
from .models import *
from .serializers import *
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

# Create your views here.

class DirectoryListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DirectorySerializer

    def get_queryset(self):
        return Directory.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    
class DirectoryDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated, IsOwner]
    serializer_class = DirectorySerializer
    queryset = Directory.objects.all()

    def get_queryset(self):
        # Always filter by the user first for security
        return Directory.objects.filter(owner=self.request.user)


class FileListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FileSerializer

    def get_queryset(self):
        # REQUIREMENT: Users access only their own files
        return File.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        # Automatically assign the logged-in user as the owner
        serializer.save(owner=self.request.user)


class FileDownloadView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated, IsOwner] # IsOwner triggers 403 if check fails
    queryset = File.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object() # This calls IsOwner check
        
        # Open the file and return as a downloadable response
        file_handle = instance.file.open()
        response = FileResponse(file_handle, content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{instance.file.name}"'
        return response