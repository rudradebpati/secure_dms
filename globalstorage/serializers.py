from django.core.validators import FileExtensionValidator
from rest_framework import serializers
from .models import *
from . import services
from django.urls import reverse
import os
from .models import File


class FileSerializer(serializers.ModelSerializer):
    file = serializers.FileField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            allowed_extensions = services.get_user_allowed_extensions(request.user)
            self.fields["file"].validators.append(
                FileExtensionValidator(allowed_extensions=allowed_extensions)
            )

    def validate_folder(self, folder):
        # Ensure the folder belongs to the user
        if folder.owner != self.context["request"].user:
            raise serializers.ValidationError("You do not own this folder.")
        return folder

    def create(self, validated_data):
        user = self.context["request"].user
        uploaded_file = validated_data["file"]

        # Dynamically calculate file size and extension
        size_in_kb = uploaded_file.size / 1024
        validated_data["name"] = uploaded_file.name
        validated_data["size"] = size_in_kb
        extension = os.path.splitext(uploaded_file.name)[1].lstrip(".").lower()
        # Assign supported extension
        ext_obj = FileExtension.objects.filter(name=extension).first()
        if not ext_obj:
            raise serializers.ValidationError("File extension not allowed.")
        if ext_obj.size_limit and size_in_kb > ext_obj.size_limit:
            raise serializers.ValidationError(
                "File size limit for this extension exceeded."
            )
        validated_data["file_extension"] = ext_obj
        validated_data["owner"] = user
        return File.objects.create(**validated_data)

    class Meta:
        model = File
        read_only_fields = ["owner", "file_extension", "size"]
        fields = ["id", "folder", "file", "name", "size", "file_extension", "owner"]


class FileDownloadSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField(read_only=True)

    def get_file_url(self, obj):
        request = self.context.get("request")
        # FileDownloadView is registered with name 'file-download'
        return request.build_absolute_uri(reverse("file-download", args=[obj.pk]))

    class Meta:
        model = File
        fields = ["file", "name", "file_url"]


class ImmediateDirectoriesSerializer(serializers.ModelSerializer):
    # This serializer is written to only load surface level of folder and files,
    # to prevent loading all nested level of folder and files recursively by main serializer.
    class Meta:
        model = Directory
        fields = ["id", "name", "parent", "owner"]


class DirectorySerializer(serializers.ModelSerializer):
    contained_files = serializers.SerializerMethodField()
    sub_folders = serializers.SerializerMethodField()

    def get_contained_files(self, obj):
        return FileSerializer(obj.files.all(), many=True).data

    def get_sub_folders(self, obj):
        children = Directory.objects.filter(parent=obj)
        return ImmediateDirectoriesSerializer(children, many=True).data

    def create(self, validated_data):
        login_user = self.context["request"].user
        dir_id = self.context["view"].kwargs.get("dir_id")
        if dir_id:
            try:
                dir_obj = Directory.objects.get(id=dir_id)
                if dir_obj.owner != login_user:
                    raise serializers.ValidationError("You do not own this folder.")
                validated_data["parent"] = dir_obj
                validated_data["is_child"] = True
            except:
                raise serializers.ValidationError("Parent directory does not exist.")
        else:
            validated_data["is_child"] = False
        return super().create(validated_data)

    class Meta:
        model = Directory
        read_only_fields = ["owner", "is_child"]
        fields = [
            "id",
            "name",
            "is_child",
            "parent",
            "owner",
            "contained_files",
            "sub_folders",
        ]
