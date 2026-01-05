from django.db import models
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class BaseAbstractModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True

class Directory(BaseAbstractModel):
    name = models.CharField(max_length=255)
    is_child = models.BooleanField(default=False)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("name", "owner")  # unique folder name for each user
        db_table="globalstorage_directories"

class FileExtension(models.Model):
    name = models.CharField(max_length=255)
    size_limit=models.IntegerField(default=0)    # in KB, 0 for no limit
    description=models.CharField(max_length=255)

    class Meta:
        db_table="globalstorage_file_extension"

class File(BaseAbstractModel):
    name=models.CharField(max_length=255)
    folder = models.ForeignKey(
        Directory, on_delete=models.CASCADE, related_name="files"
    )
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to="uploads/")
    size=models.IntegerField(default=0) # in KB
    file_extension=models.ForeignKey(FileExtension, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table="globalstorage_files"


class UserExtensionMap(BaseAbstractModel):
    # Additional model to restrict user to specific extensions
    extension = models.ForeignKey(FileExtension, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    class Meta:
        # unique_together = ("extension", "user")
        db_table="globalstorage_user_extension_map"
