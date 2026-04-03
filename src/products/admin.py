from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import (
    Manufacturer,
    ComicBookProduct,
    ToyProduct,
    ClothesProduct,
    AccessoryProduct,
    HomeDecorProduct,
    ProductTranslation,
    ProductImage,
    Warehouse,
    Review,
)


class ManufacturerAdmin(admin.ModelAdmin):
    """ Manufacturer Model for admin """
    ordering = ('name',)
    list_display = ('__str__', 'slug')
    prepopulated_fields = {'slug': ('name',)}


class PriceListFilter(admin.SimpleListFilter):
    title = _('Price category')
    parameter_name = 'price'
    
    def lookups(self, request, model_admin):
        return (
            ('low', _('Low price')),
            ('medium', _('Average price')),
            ('high', _('High price')),
        )
    
    def queryset(self, request, queryset):
        val = self.value()
        if val == 'low':
            return queryset.filter(price__lt=10)
        elif val == 'medium':
            return queryset.filter(price__gte=10, price__lte=100)
        elif val == 'high':
            return queryset.filter(price__gt=100)


def null_old_price(modeladmin, request, queryset):
    """ Reset old product prices for admin """
    for rec in queryset:
        rec.old_price = 0.0
        rec.save()
    modeladmin.message_user(request, _('Old prices have been reset'))
null_old_price.short_description = _('Reset old prices')


class ProductTranslationInline(admin.StackedInline):
    model = ProductTranslation
    extra = 0


class ProductImageInline(admin.TabularInline):
    model = ProductImage


class WarehouseInline(admin.TabularInline):
    model = Warehouse
    extra = 0


class ComicBookProductAdmin(admin.ModelAdmin):
    """ ComicBookProduct Model for admin """
    list_display = (
        '__str__',
        'manufacturer',
        'category',
        'price',
        'old_price',
        'rating',
        'published',
        'created_at',
        'updated_at',
    )
    list_filter = ('manufacturer', 'category', PriceListFilter)
    search_fields = ('id', 'name', 'description')
    actions = (null_old_price,)
    save_on_top = True
    prepopulated_fields = {'slug': ('name',)}
    fieldsets = (
        (_('Product'), {
            'fields': (
                'manufacturer',
                'name',
                'slug',
                'main_image',
                ('price', 'old_price'),
                'rating',
            ),
        }),
        (_('Metadata'), {
            'fields': ('meta_description', 'meta_keywords'),
        }),
        (_('Description / Specifications'), {
            'fields': (
                'description',
                'category',
                'publication_format',
                'number_pages',
                'published',
                'binding',
                'language',
            ),
        }),
    )
    readonly_fields = ('rating',)
    inlines = (ProductTranslationInline, ProductImageInline, WarehouseInline)


class ToyProductAdmin(admin.ModelAdmin):
    """ ToyProduct Model for admin """
    list_display = (
        '__str__',
        'manufacturer',
        'category',
        'price',
        'old_price',
        'rating',
        'created_at',
        'updated_at',
    )
    list_filter = ('manufacturer', 'category', PriceListFilter)
    search_fields = ('id', 'name', 'description')
    actions = (null_old_price,)
    save_on_top = True
    prepopulated_fields = {'slug': ('name',)}
    fieldsets = (
        (_('Product'), {
            'fields': (
                'manufacturer',
                'name',
                'slug',
                'main_image',
                ('price', 'old_price'),
                'rating',
            ),
        }),
        (_('Metadata'), {
            'fields': ('meta_description', 'meta_keywords'),
        }),
        (_('Description / Specifications'), {
            'fields': (
                'description',
                'category',
                'country',
                'material',
                'packing_size',
                'weight',
            ),
        }),
    )
    readonly_fields = ('rating',)
    inlines = (ProductTranslationInline, ProductImageInline, WarehouseInline)


class ClothesProductAdmin(admin.ModelAdmin):
    """ ClothesProduct Model for admin """
    list_display = (
        '__str__',
        'manufacturer',
        'category',
        'price',
        'old_price',
        'rating',
        'created_at',
        'updated_at',
    )
    list_filter = ('manufacturer', 'category', PriceListFilter)
    search_fields = ('id', 'name', 'description')
    actions = (null_old_price,)
    save_on_top = True
    prepopulated_fields = {'slug': ('name',)}
    fieldsets = (
        (_('Product'), {
            'fields': (
                'manufacturer',
                'name',
                'slug',
                'main_image',
                ('price', 'old_price'),
                'rating',
            ),
        }),
        (_('Metadata'), {
            'fields': ('meta_description', 'meta_keywords'),
        }),
        (_('Description / Specifications'), {
            'fields': (
                'description',
                'category',
                'size',
                'color',
            ),
        }),
    )
    readonly_fields = ('rating',)
    inlines = (ProductTranslationInline, ProductImageInline, WarehouseInline)


class AccessoryProductAdmin(admin.ModelAdmin):
    """ AccessoryProduct Model for admin """
    list_display = (
        '__str__',
        'manufacturer',
        'category',
        'price',
        'old_price',
        'rating',
        'created_at',
        'updated_at',
    )
    list_filter = ('manufacturer', 'category', PriceListFilter)
    search_fields = ('id', 'name', 'description')
    actions = (null_old_price,)
    save_on_top = True
    prepopulated_fields = {'slug': ('name',)}
    fieldsets = (
        (_('Product'), {
            'fields': (
                'manufacturer',
                'name',
                'slug',
                'main_image',
                ('price', 'old_price'),
                'rating',
            ),
        }),
        (_('Metadata'), {
            'fields': ('meta_description', 'meta_keywords'),
        }),
        (_('Description / Specifications'), {
            'fields': (
                'description',
                'category',
            ),
        }),
    )
    readonly_fields = ('rating',)
    inlines = (ProductTranslationInline, ProductImageInline, WarehouseInline)


class HomeDecorProductAdmin(admin.ModelAdmin):
    """ HomeDecorProduct Model for admin """
    list_display = (
        '__str__',
        'manufacturer',
        'category',
        'price',
        'old_price',
        'rating',
        'created_at',
        'updated_at',
    )
    list_filter = ('manufacturer', 'category', PriceListFilter)
    search_fields = ('id', 'name', 'description')
    actions = (null_old_price,)
    save_on_top = True
    prepopulated_fields = {'slug': ('name',)}
    fieldsets = (
        (_('Product'), {
            'fields': (
                'manufacturer',
                'name',
                'slug',
                'main_image',
                ('price', 'old_price'),
                'rating',
            ),
        }),
        (_('Metadata'), {
            'fields': ('meta_description', 'meta_keywords'),
        }),
        (_('Description / Specifications'), {
            'fields': (
                'description',
                'category',
            ),
        }),
    )
    readonly_fields = ('rating',)
    inlines = (ProductTranslationInline, ProductImageInline, WarehouseInline)


class ReviewAdmin(admin.ModelAdmin):
    """ Review Model for admin """
    list_display = ('id', 'product', 'user', 'rating', 'created_at')
    filter_horizontal = ('likes', 'dislikes')
    readonly_fields = ('created_at',)


admin.site.register(Manufacturer, ManufacturerAdmin)
admin.site.register(ComicBookProduct, ComicBookProductAdmin)
admin.site.register(ToyProduct, ToyProductAdmin)
admin.site.register(ClothesProduct, ClothesProductAdmin)
admin.site.register(AccessoryProduct, AccessoryProductAdmin)
admin.site.register(HomeDecorProduct, HomeDecorProductAdmin)
admin.site.register(Review, ReviewAdmin)
