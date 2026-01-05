from .models import UserExtensionMap


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
    return ext_list
