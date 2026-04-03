from os.path import splitext
from django.utils import timezone


def get_manufacturer_logo_path(instance, filename):
    """ Get path of manufacturer logo """
    path_name = timezone.now().timestamp()
    file_ext = splitext(filename)[1].lower()
    return f'manufacturers/{ path_name }{ file_ext }'


def get_product_image_path(instance, filename):
    """ Get path of product image """
    path_name = timezone.now().strftime('%Y/%m/%d/%H%M%S%f')
    file_ext = splitext(filename)[1].lower()
    return f'products/{ path_name }{ file_ext }'
