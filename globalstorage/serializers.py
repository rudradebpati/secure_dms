from django.core.validators import FileExtensionValidator
from rest_framework import serializers
from .models import *
from . import services
from django.urls import reverse


class FileSerializer(serializers.ModelSerializer):
    file = serializers.FileField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        allowed_extensions = services.get_user_allowed_extensions(
            self.context.get("request").user
        )
        self.fields["file"].validators.append(
            FileExtensionValidator(allowed_extensions=allowed_extensions)
        )

    def validate_folder(self, obj):
        # Ensure the folder belongs to the user
        if obj.owner != self.context["request"].user:
            raise serializers.ValidationError("You do not own this folder.")
        return obj

    class Meta:
        model = File
        fields = ["id", "folder", "file", "name", "size"]

class FileDownloadSerializer(serializers.ModelSerializer):
    file_url=serializers.SerializerMethodField(read_only=True)

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
