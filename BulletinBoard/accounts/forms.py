from allauth.account.forms import SignupForm, LoginForm
from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _, pgettext_lazy


class CustomSignupForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget = forms.TextInput(attrs={
            'class': 'form-control my-2 text-bg-dark fs-5',
            "placeholder": _("Username"),
            "autocomplete": "username"
        })
        self.fields['email'].widget = forms.TextInput(attrs={
            "class": 'form-control my-2 text-bg-dark fs-5',
            "type": "email",
            "placeholder": _("Email address"),
            "autocomplete": "email",
        })
        self.fields['email'].label = _('Email')
        self.fields['password1'].widget = forms.PasswordInput(attrs={
            'class': 'form-control my-2 text-bg-dark fs-5',
            'placeholder': _('Password')
        })
        self.fields['password2'].widget = forms.PasswordInput(attrs={
            'class': 'form-control my-2 text-bg-dark fs-5',
            'placeholder': _('Repeat password')
        })


class CustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['login'].widget = forms.TextInput(attrs={
            'class': 'form-control my-2 text-bg-dark fs-5',
            'placeholder': _('Username or email'),
            "autocomplete": "email"
        })
        self.fields['login'].label = pgettext_lazy('noun', 'Login')
        self.fields['password'].widget = forms.PasswordInput(attrs={
            'class': 'form-control my-2 text-bg-dark fs-5',
            'placeholder': _('Password')
        })
        self.fields['remember'].widget = forms.CheckboxInput(attrs={'class': 'form-check-input my-2 text-bg-dark fs-5'})


class ProfileForm(forms.ModelForm):
    username = forms.CharField(disabled=True, label=_('Username'),
                               widget=forms.TextInput(attrs={'class': 'form-control my-2 text-bg-dark fs-5'}))
    email = forms.CharField(disabled=True, label=_('Email'),
                            widget=forms.TextInput(attrs={'class': 'form-control my-2 text-bg-dark fs-5'}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name']
        labels = {
            'first_name': _('First name'),
            'last_name': _('Last name'),
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control mb-2 mt-2 text-bg-dark fs-5'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control mb-2 mt-2 text-bg-dark fs-5'})
        }