from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model


class RegistrationForm(forms.ModelForm):
    username = forms.CharField(
        label="Логин",
        min_length=4,
        max_length=64,
        widget=forms.TextInput(
            attrs={
                "class": "form-control mb-3",
                "placeholder": "Логин киритинг",
            }
        ),
    )
    first_name = forms.CharField(
        label="Исм",
        max_length=128,
        widget=forms.TextInput(
            attrs={
                "class": "form-control mb-3",
                "placeholder": "Исмни киритинг",
            }
        ),
    )
    last_name = forms.CharField(
        label="Фамилия",
        max_length=128,
        widget=forms.TextInput(
            attrs={
                "class": "form-control mb-3",
                "placeholder": "Фамилияни киритинг",
            }
        ),
    )
    password = forms.CharField(
        label="Парол",
        min_length=8,
        max_length=64,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control mb-3",
                "placeholder": "Парол киритинг",
            }
        ),
    )
    password2 = forms.CharField(
        label="Паролни бошидан киритинг",
        min_length=8,
        max_length=64,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control mb-3",
                "placeholder": "Паролни бошидан киритинг",
            }
        ),
    )

    def clean_password2(self):
        if self.cleaned_data["password"] == self.cleaned_data["password2"]:
            return self.cleaned_data["password2"]
        else:
            raise forms.ValidationError(_("Passwords are different"))

    class Meta:
        model = get_user_model()
        fields = ("username", "first_name", "last_name")


class LoginForm(forms.Form):
    username = forms.CharField(
        label="Логин",
        min_length=4,
        max_length=64,
        widget=forms.TextInput(
            attrs={
                "class": "form-control mb-3",
                "placeholder": "Логин киритинг",
            }
        ),
    )
    password = forms.CharField(
        label="Парол",
        min_length=4,
        max_length=64,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control mb-3",
                "placeholder": "Паролни киритинг",
            }
        ),
    )


class EditAccountForm(forms.ModelForm):
    username = forms.CharField(
        label="Логин",
        min_length=4,
        max_length=64,
        widget=forms.TextInput(
            attrs={
                "class": "form-control mb-3",
                "placeholder": "Логин киритинг",
                "readonly": True,
            }
        ),
    )
    first_name = forms.CharField(
        label="Исм",
        max_length=128,
        widget=forms.TextInput(
            attrs={
                "class": "form-control mb-3",
                "placeholder": "Исмни киритинг",
            }
        ),
    )
    last_name = forms.CharField(
        label="Фамилия",
        max_length=128,
        widget=forms.TextInput(
            attrs={
                "class": "form-control mb-3",
                "placeholder": "Фамилияни киритинг",
            }
        ),
    )

    class Meta:
        model = get_user_model()
        fields = ("username", "first_name", "last_name")
