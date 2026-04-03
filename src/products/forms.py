from django import forms
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from .models import ComicBookProduct, ToyProduct, ClothesProduct
from .models import AccessoryProduct, HomeDecorProduct, Review


class SortingForm(forms.Form):
    """ Sorting Form """
    TYPE_SORT_CHOICES = [
        ('popularity', _('Popularity')),
        ('new_old', _('New - Old')),
        ('old_new', _('Old - New')),
        ('low_high_price', _('Low - High Price')),
        ('high_low_price', _('High - Low Price')),
        ('az_order', _('A - Z Order')),
        ('za_order', _('Z - A Order')),
    ]
    type_sort = forms.ChoiceField(
        label=_('Sort by:'),
        choices=TYPE_SORT_CHOICES,
        widget=forms.widgets.Select(
            attrs={
                'class': 'form-control custom-select',
                'onchange': 'location=this.value;',
            },
        ),
        required=False,
    )


class ManufacturerFilter(forms.Form):
    """ Manufacturer Filter """
    min_price = forms.CharField(
        label=_('Min price'),
        widget=forms.widgets.TextInput(
            attrs={
                'class': 'form-control cz-range-slider-value-min',
            },
        ),
        required=False,
    )
    max_price = forms.CharField(
        label=_('Max price'),
        widget=forms.widgets.TextInput(
            attrs={
                'class': 'form-control cz-range-slider-value-max',
            },
        ),
        required=False,
    )
    
    CATEGORY_CHOICES = [
        ('1', _('Comics')),
        ('2', _('Toys')),
        ('3', _('Clothes')),
        ('4', _('Accessories')),
        ('5', _('Home Decor')),
    ]
    categories = forms.MultipleChoiceField(
        label=_('Categories'),
        choices=CATEGORY_CHOICES,
        widget=forms.widgets.CheckboxSelectMultiple(
            attrs={
                'class': 'custom-control-input',
            },
        ),
        required=False,
    )


class ComicBookFilter(forms.Form):
    """ Comic Book Filter """
    min_price = forms.CharField(
        label=_('Min price'),
        widget=forms.widgets.TextInput(
            attrs={
                'class': 'form-control cz-range-slider-value-min',
            },
        ),
        required=False,
    )
    max_price = forms.CharField(
        label=_('Max price'),
        widget=forms.widgets.TextInput(
            attrs={
                'class': 'form-control cz-range-slider-value-max',
            },
        ),
        required=False,
    )
    
    categories = forms.MultipleChoiceField(
        label=_('Categories'),
        choices=ComicBookProduct.CATEGORY_CHOICES[1:],
        widget=forms.widgets.CheckboxSelectMultiple(
            attrs={
                'class': 'custom-control-input',
            },
        ),
        required=False,
    )

    languages = forms.MultipleChoiceField(
        label=_('Languages'),
        choices=settings.LANGUAGES,
        widget=forms.widgets.CheckboxSelectMultiple(
            attrs={
                'class': 'custom-control-input',
            },
        ),
        required=False,
    )


class ToyFilter(forms.Form):
    """ Toy Filter """
    min_price = forms.CharField(
        label=_('Min price'),
        widget=forms.widgets.TextInput(
            attrs={
                'class': 'form-control cz-range-slider-value-min',
            },
        ),
        required=False,
    )
    max_price = forms.CharField(
        label=_('Max price'),
        widget=forms.widgets.TextInput(
            attrs={
                'class': 'form-control cz-range-slider-value-max',
            },
        ),
        required=False,
    )
    
    categories = forms.MultipleChoiceField(
        label=_('Categories'),
        choices=ToyProduct.CATEGORY_CHOICES[1:],
        widget=forms.widgets.CheckboxSelectMultiple(
            attrs={
                'class': 'custom-control-input',
            },
        ),
        required=False,
    )
    countries = forms.MultipleChoiceField(
        label=_('Countries'),
        choices=ToyProduct.COUNTRY_CHOICES[1:],
        widget=forms.widgets.CheckboxSelectMultiple(
            attrs={
                'class': 'custom-control-input',
            },
        ),
        required=False,
    )
    materials = forms.MultipleChoiceField(
        label=_('Materials'),
        choices=ToyProduct.MATERIAL_CHOICES[1:],
        widget=forms.widgets.CheckboxSelectMultiple(
            attrs={
                'class': 'custom-control-input',
            },
        ),
        required=False,
    )


class ClothesFilter(forms.Form):
    """ Clothes Filter """
    min_price = forms.CharField(
        label=_('Min price'),
        widget=forms.widgets.TextInput(
            attrs={
                'class': 'form-control cz-range-slider-value-min',
            },
        ),
        required=False,
    )
    max_price = forms.CharField(
        label=_('Max price'),
        widget=forms.widgets.TextInput(
            attrs={
                'class': 'form-control cz-range-slider-value-max',
            },
        ),
        required=False,
    )
    
    categories = forms.MultipleChoiceField(
        label=_('Categories'),
        choices=ClothesProduct.CATEGORY_CHOICES[1:],
        widget=forms.widgets.CheckboxSelectMultiple(
            attrs={
                'class': 'custom-control-input',
            },
        ),
        required=False,
    )
    sizes = forms.MultipleChoiceField(
        label=_('Sizes'),
        choices=ClothesProduct.SIZE_CHOICES[1:],
        widget=forms.widgets.CheckboxSelectMultiple(
            attrs={
                'class': 'custom-control-input',
            },
        ),
        required=False,
    )
    colors = forms.MultipleChoiceField(
        label=_('Colors'),
        choices=ClothesProduct.COLOR_CHOICES[1:],
        widget=forms.widgets.CheckboxSelectMultiple(
            attrs={
                'class': 'custom-control-input',
            },
        ),
        required=False,
    )


class AccessoryFilter(forms.Form):
    """ Accessory Filter """
    min_price = forms.CharField(
        label=_('Min price'),
        widget=forms.widgets.TextInput(
            attrs={
                'class': 'form-control cz-range-slider-value-min',
            },
        ),
        required=False,
    )
    max_price = forms.CharField(
        label=_('Max price'),
        widget=forms.widgets.TextInput(
            attrs={
                'class': 'form-control cz-range-slider-value-max',
            },
        ),
        required=False,
    )
    
    categories = forms.MultipleChoiceField(
        label=_('Categories'),
        choices=AccessoryProduct.CATEGORY_CHOICES[1:],
        widget=forms.widgets.CheckboxSelectMultiple(
            attrs={
                'class': 'custom-control-input',
            },
        ),
        required=False,
    )


class HomeDecorFilter(forms.Form):
    """ Home Decor Filter """
    min_price = forms.CharField(
        label=_('Min price'),
        widget=forms.widgets.TextInput(
            attrs={
                'class': 'form-control cz-range-slider-value-min',
            },
        ),
        required=False,
    )
    max_price = forms.CharField(
        label=_('Max price'),
        widget=forms.widgets.TextInput(
            attrs={
                'class': 'form-control cz-range-slider-value-max',
            },
        ),
        required=False,
    )
    
    categories = forms.MultipleChoiceField(
        label=_('Categories'),
        choices=HomeDecorProduct.CATEGORY_CHOICES[1:],
        widget=forms.widgets.CheckboxSelectMultiple(
            attrs={
                'class': 'custom-control-input',
            },
        ),
        required=False,
    )


class ReviewForm(forms.ModelForm):
    """ Review Form """

    class Meta:
        model = Review
        fields = ['rating', 'comment']
        help_texts = {
            'comment': _('Please leave review meaningful and useful.')
        }
        widgets = {
            'rating': forms.widgets.Select(attrs={'class': 'custom-select'}),
            'comment': forms.widgets.Textarea(attrs={'placeholder': ''}),
        }
