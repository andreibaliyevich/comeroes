from django.core.exceptions import ValidationError
from django.core.files.images import ImageFile
from django.utils.translation import gettext_lazy as _


class MinSizeImageValidator:
    """ Minimum image size checker """

    def __init__(self, min_width, min_height):
        self.min_width = min_width
        self.min_height = min_height

    def __call__(self, image):
        image = ImageFile(image)

        if image.width < self.min_width or image.height < self.min_height:
            error_str = _('Error! Size of your image:')
            raise ValidationError(f'{ error_str } { image.width } x { image.height }.')
