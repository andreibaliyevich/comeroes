from os.path import splitext
from django.utils import timezone


def get_store_image_path(instance, filename):
    """ Get path of store image """
    path_name = timezone.now().timestamp()
    file_ext = splitext(filename)[1].lower()
    return f'store/{ path_name }{ file_ext }'
