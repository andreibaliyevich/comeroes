from django.conf import settings
from django.db import models
from django.db.models import Avg, Value
from django.db.models.functions import Coalesce
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from main.model_fields import TranslatedField
from contacts.models import Store
from .managers import ProductManager
from .utilities import get_manufacturer_logo_path, get_product_image_path


class Manufacturer(models.Model):
    """ Manufacturer Model """
    name = models.CharField(max_length=64, verbose_name=_('Name'))
    slug = models.SlugField(max_length=64, unique=True, verbose_name=_('Slug'))

    logo = models.ImageField(
        upload_to=get_manufacturer_logo_path,
        help_text=_('Recommend: 300 x 160 px.'),
        verbose_name=_('Logo'),
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('products:manufacturer', args=[self.slug])

    class Meta:
        verbose_name = _('Manufacturer')
        verbose_name_plural = _('Manufacturers')
        ordering = ['name']


class Product(models.Model):
    """ Product Model """
    manufacturer = models.ForeignKey(
        Manufacturer,
        on_delete=models.PROTECT,
        verbose_name=_('Manufacturer'),
    )

    name = models.CharField(max_length=255, verbose_name=_('Name'))
    translated_name = TranslatedField('name')
    slug = models.SlugField(max_length=255, unique=True, verbose_name=_('Slug'))

    meta_description = models.CharField(
        blank=True,
        max_length=255,
        verbose_name=_('Description'),
    )
    meta_keywords = models.CharField(
        blank=True,
        max_length=255,
        help_text=_('Separate keywords with commas.'),
        verbose_name=_('Keywords'),
    )
    translated_meta_description = TranslatedField('meta_description')
    translated_meta_keywords = TranslatedField('meta_keywords')

    main_image = models.ImageField(
        upload_to=get_product_image_path,
        verbose_name=_('Main image'),
        help_text=_('Recommend: 764 x 905 px.'),
    )

    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0.0,
        verbose_name=_('Price'),
    )
    old_price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0.0,
        verbose_name=_('Old price'),
    )

    rating = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        default=0.0,
        verbose_name=_('Rating'),
    )

    description = models.TextField(blank=True, verbose_name=_('Description'))
    translated_description = TranslatedField('description')

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Created at'),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Updated at'),
    )

    objects = ProductManager()

    def get_absolute_url(self):
        return reverse('products:product_detail', args=[self.id])

    def __str__(self):
        return f'{ self.id } | { self.translated_name }'


class ComicBookProduct(Product):
    """ Comic Book Product Model """
    CATEGORY_CHOICES = [
        ('', _('Select category')),
        ('1', _('Marvel')),
        ('2', _('DC')),
        ('3', _('Star Wars')),
    ]
    category = models.CharField(
        blank=True,
        max_length=1,
        choices=CATEGORY_CHOICES,
        default='',
        verbose_name=_('Category'),
    )

    publication_format = models.CharField(
        blank=True,
        max_length=16,
        verbose_name=_('Publication format'),
    )
    number_pages = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        verbose_name=_('Number of pages'),
    )
    published = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('Published'),
    )

    BINDING_CHOICES = [
        ('', _('Select binding')),
        ('1', _('Paperback')),
        ('2', _('Hardcover')),
    ]
    binding = models.CharField(
        blank=True,
        max_length=1,
        choices=BINDING_CHOICES,
        default='',
        verbose_name=_('Binding'),
    )

    language = models.CharField(
        max_length=2,
        choices=settings.LANGUAGES,
        default=settings.LANGUAGE_CODE,
        verbose_name=_('Language'),
    )

    def get_absolute_url(self):
        return reverse('products:comic_book_detail', args=[self.slug])

    class Meta:
        verbose_name = _('Comic Book')
        verbose_name_plural = _('Comics')
        ordering = ['-created_at', '-updated_at', '-id']


class ToyProduct(Product):
    """ Toy Product Model """
    CATEGORY_CHOICES = [
        ('', _('Select category')),
        ('1', _('Marvel')),
        ('2', _('DC')),
        ('3', _('Star Wars')),
    ]
    category = models.CharField(
        blank=True,
        max_length=1,
        choices=CATEGORY_CHOICES,
        default='',
        verbose_name=_('Category'),
    )

    COUNTRY_CHOICES = [
        ('', _('Select country')),
        ('US', _('USA')),
        ('CN', _('China')),
        ('RU', _('Russia')),
    ]
    country = models.CharField(
        blank=True,
        max_length=2,
        choices=COUNTRY_CHOICES,
        default='',
        verbose_name=_('Manufacturer country'),
    )

    MATERIAL_CHOICES = [
        ('', _('Select material')),
        ('1', _('Plastic')),
        ('2', _('Plastic / electronics')),
        ('3', _('Plastic / LED')),
        ('4', _('Polyester')),
        ('5', _('Plush')),
    ]
    material = models.CharField(
        blank=True,
        max_length=1,
        choices=MATERIAL_CHOICES,
        default='',
        verbose_name=_('Material'),
    )

    packing_size = models.CharField(
        blank=True,
        max_length=32,
        verbose_name=_('Packing size'),
        help_text=_('millimetres'),
    )
    weight = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        verbose_name=_('Weight'),
        help_text=_('gram'),
    )

    def get_absolute_url(self):
        return reverse('products:toy_detail', args=[self.slug])

    class Meta:
        verbose_name = _('Toy')
        verbose_name_plural = _('Toys')
        ordering = ['-created_at', '-updated_at', '-id']


class ClothesProduct(Product):
    """ Clothes Product Model """
    CATEGORY_CHOICES = [
        ('', _('Select category')),
        ('1', _('T-Shirts')),
        ('2', _('Jackets & Sweatshirts')),
        ('3', _('Robes & Sleepwear')),
        ('4', _('Kids & Baby')),
        ('5', _('Tank Tops')),
    ]
    category = models.CharField(
        blank=True,
        max_length=1,
        choices=CATEGORY_CHOICES,
        default='',
        verbose_name=_('Category'),
    )

    SIZE_CHOICES = [
        ('', _('Select size')),
        ('XS', _('X-Small')),
        ('S', _('Small')),
        ('M', _('Medium')),
        ('L', _('Large')),
        ('XL', _('X-Large')),
        ('XXL', _('XX-Large')),
        ('XXXL', _('XXX-Large')),
    ]
    size = models.CharField(
        blank=True,
        max_length=4,
        choices=SIZE_CHOICES,
        default='',
        verbose_name=_('Size'),
    )

    COLOR_CHOICES = [
        ('', _('Select color')),
        ('ff0000', _('Red')),
        ('00ff00', _('Green')),
        ('0000ff', _('Blue')),
        ('000000', _('Black')),
        ('ffffff', _('White')),
        ('808080', _('Gray')),
        ('ffc0cb', _('Pink')),
        ('800080', _('Purple')),
    ]
    color = models.CharField(
        blank=True,
        max_length=6,
        choices=COLOR_CHOICES,
        default='',
        verbose_name=_('Color'),
    )

    def get_absolute_url(self):
        return reverse('products:clothes_detail', args=[self.slug])

    class Meta:
        verbose_name = _('Clothes')
        verbose_name_plural = _('Clothes')
        ordering = ['-created_at', '-updated_at', '-id']


class AccessoryProduct(Product):
    """ Accessory Product Model """
    CATEGORY_CHOICES = [
        ('', _('Select category')),
        ('1', _('Bags & Backpacks')),
        ('2', _('Jewelry')),
        ('3', _('Tech Accessories')),
        ('4', _('Travel Accessories')),
        ('5', _('Hats')),
        ('6', _('Scarves')),
        ('7', _('Socks')),
    ]
    category = models.CharField(
        blank=True,
        max_length=1,
        choices=CATEGORY_CHOICES,
        default='',
        verbose_name=_('Category'),
    )

    def get_absolute_url(self):
        return reverse('products:accessory_detail', args=[self.slug])

    class Meta:
        verbose_name = _('Accessory')
        verbose_name_plural = _('Accessories')
        ordering = ['-created_at', '-updated_at', '-id']


class HomeDecorProduct(Product):
    """ Home Decor Product Model """
    CATEGORY_CHOICES = [
        ('', _('Select category')),
        ('1', _('Mugs')),
        ('2', _('Ornaments & Holiday Decor')),
        ('3', _('Posters & Prints')),
        ('4', _('Stationery')),
    ]
    category = models.CharField(
        blank=True,
        max_length=1,
        choices=CATEGORY_CHOICES,
        default='',
        verbose_name=_('Category'),
    )

    def get_absolute_url(self):
        return reverse('products:home_decor_detail', args=[self.slug])

    class Meta:
        verbose_name = _('Home Decor')
        verbose_name_plural = _('Home Decor')
        ordering = ['-created_at', '-updated_at', '-id']


class ProductTranslation(models.Model):
    """ Product Translation Model """
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='translations',
        verbose_name=_('Product'),
    )
    language = models.CharField(
        max_length=2,
        choices=settings.LANGUAGES[1:],
        verbose_name=_('Language'),
    )

    name = models.CharField(max_length=255, verbose_name=_('Name'))

    meta_description = models.CharField(
        blank=True,
        max_length=255,
        verbose_name=_('Description'),
    )
    meta_keywords = models.CharField(
        blank=True,
        max_length=255,
        help_text=_('Separate keywords with commas.'),
        verbose_name=_('Keywords'),
    )

    description = models.TextField(blank=True, verbose_name=_('Description'))

    class Meta:
        verbose_name = _('Product Translation')
        verbose_name_plural = _('Product Translations')
        ordering = ['product', 'language']
        unique_together = ['product', 'language']


class ProductImage(models.Model):
    """ Product Image Model """
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name=_('Product'),
    )
    image = models.ImageField(
        upload_to=get_product_image_path,
        verbose_name=_('Image'),
        help_text=_('Recommend: 764 x 905 px.'),
    )

    class Meta:
        verbose_name = _('Product Image')
        verbose_name_plural = _('Product Images')
        ordering = ['product', 'id']


class Warehouse(models.Model):
    """ Warehouse Model """
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name=_('Product'),
    )
    store = models.ForeignKey(
        Store,
        on_delete=models.CASCADE,
        verbose_name=_('Store'),
    )
    count = models.PositiveIntegerField(verbose_name=_('Count'))

    class Meta:
        verbose_name = _('Warehouse')
        verbose_name_plural = _('Warehouses')
        ordering = ['product', 'store']
        unique_together = ['product', 'store']


class Review(models.Model):
    """ Review Model """
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name=_('Product'),
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_('User'),
    )

    RATING_CHOICES = [
        (None, _('Choose rating')),
        (5, _('5 stars')),
        (4, _('4 stars')),
        (3, _('3 stars')),
        (2, _('2 stars')),
        (1, _('1 star')),
    ]
    rating = models.IntegerField(
        choices=RATING_CHOICES,
        verbose_name=_('Rating'),
    )

    comment = models.TextField(verbose_name=_('Comment'))
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Created at'),
    )

    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name='review_likes',
        verbose_name=_('Likes'),
    )
    dislikes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name='review_dislikes',
        verbose_name=_('Dislikes'),
    )

    class Meta:
        verbose_name = _('Review')
        verbose_name_plural = _('Reviews')
        ordering = ['-created_at', '-id']
        unique_together = ['product', 'user']


@receiver(post_save, sender=Review)
@receiver(post_delete, sender=Review)
def update_product_rating(sender, **kwargs):
    """ Update product rating """
    product = kwargs['instance'].product
    product_rating = product.review_set.aggregate(
        total_rating=Coalesce(Avg('rating'), Value(0.0)))
    product.rating = product_rating['total_rating']
    product.save()
