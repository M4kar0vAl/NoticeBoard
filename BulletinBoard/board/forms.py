from django import forms
from django.utils.translation import gettext_lazy as _, pgettext_lazy

from tinymce.widgets import TinyMCE

from .models import Advert, Response


class AdvertForm(forms.ModelForm):
    title = forms.CharField(
        label=_('Title'),
        widget=forms.TextInput(attrs={'class': 'form-control mb-2 mt-2 text-bg-dark fs-5'})
    )
    text = forms.CharField(
        widget=TinyMCE(),
        label=pgettext_lazy('content of the advertisement', 'Content')
    )
    category = forms.ChoiceField(
        label=_('Category'),
        choices=Advert.CATEGORY_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select mb-2 mt-2 text-bg-dark fs-5'})
    )

    class Meta:
        model = Advert
        fields = [
            'title',
            'text',
            'category',
        ]
    

class ResponseForm(forms.ModelForm):
    text = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control my-2 text-bg-dark mx-auto fs-5',
                'style': 'height: 250px; width: 600px',
            }
        ),
        label=pgettext_lazy('content of the response', 'Content')
    )

    class Meta:
        model = Response
        fields = [
            'text',
        ]
