from .models import UserExtensionMap, FileExtension


def get_user_allowed_extensions(user_obj):
    """
    Returns a list of file extensions that the given user is allowed to upload.

    Parameters:
    user_obj (User): The user object to check allowed extensions for.

    Returns:
    list: A list of allowed file extensions.
    """
    ext_list = list(
        UserExtensionMap.objects.filter(user=user_obj).values_list(
            "extension__name", flat=True
        )
    )
    if not ext_list:    # If a user is not assigned with extension Allow him all available extensions
        return list(FileExtension.objects.all().values_list("name", flat=True))
    return ext_list
