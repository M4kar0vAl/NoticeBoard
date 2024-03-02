import django_filters
from django import forms
from django.utils.translation import gettext_lazy as _
from django.utils.translation import pgettext_lazy

from .models import Response, Advert


class ResponseFilter(django_filters.FilterSet):
    advert__title = django_filters.CharFilter(
        lookup_expr='icontains',
        label=_('Advert title contains'),
        widget=forms.TextInput(attrs={'class': 'form-control my-2 text-bg-dark fs-5'})
    )
    advert__category = django_filters.ChoiceFilter(
        choices=Advert.CATEGORY_CHOICES,
        label=_('Category'),
        empty_label=None,
        widget = forms.Select(attrs={'class': 'form-select my-2 text-bg-dark fs-5'})
    )
    created = django_filters.DateTimeFilter(
        lookup_expr='gt',
        widget=forms.DateTimeInput(attrs={'type': 'date', 'class': 'form-control my-2 text-bg-dark fs-5'}),
        label=_('Published later than')
    )
    is_accepted = django_filters.BooleanFilter(
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input my-2 text-bg-dark fs-5'}),
        label=pgettext_lazy('response is accepted', 'Accepted')
    )

    class Meta:
        model = Response
        fields = ['advert__title', 'advert__category', 'created']


class AdvertFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(
        lookup_expr='icontains',
        label=_('Title contains'),
        widget=forms.TextInput(attrs={'class': 'form-control mb-2 mt-2 text-bg-dark fs-5'})
    )
    category = django_filters.ChoiceFilter(
        choices=Advert.CATEGORY_CHOICES,
        label=_('Category'),
        empty_label=None,
        widget=forms.Select(attrs={'class': 'form-select mb-2 mt-2 text-bg-dark fs-5'})
    )
    created = django_filters.DateTimeFilter(
        lookup_expr='gt',
        widget=forms.DateTimeInput(attrs={'type': 'date', 'class': 'form-control mb-2 mt-2 text-bg-dark fs-5'}),
        label=_('Published later than')
    )

    class Meta:
        model = Advert
        fields = ['title', 'category', 'created',]
