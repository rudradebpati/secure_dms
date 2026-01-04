from .models import UserExtensionMap
def get_user_allowed_extensions(user_obj):
    ext_list= list(UserExtensionMap.objects.filter(user=user_obj).values_list('extension__name', flat=True))
    return ext_list
