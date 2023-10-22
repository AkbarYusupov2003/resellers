from django import forms

from company import models


class CompanyForm(forms.ModelForm):
    name = forms.CharField(
        label="Номи",
        max_length=255,
        widget=forms.TextInput(
            attrs={
                "class": "form-control mb-3",
                "placeholder": "Номини киритинг",
            }
        ),
    )
    email = forms.EmailField(
        label="Почта",
        max_length=254,
        widget=forms.EmailInput(
            attrs={
                "class": "form-control mb-3",
                "placeholder": "Почтани киритинг",
            }
        ),
    )
    address = forms.CharField(
        label="Адрес",
        max_length=512,
        widget=forms.TextInput(
            attrs={
                "class": "form-control mb-3",
                "placeholder": "Адресни киритинг",
            }
        ),
    )
    phone_number = forms.CharField(
        label="Телефон Раками",
        max_length=16,
        widget=forms.TextInput(
            attrs={
                "class": "form-control mb-3",
                "placeholder": "Телефон ракамини киритинг",
            }
        ),
    )
    license_number = forms.CharField(
        label="Лицензия",
        max_length=32,
        widget=forms.TextInput(
            attrs={
                "class": "form-control mb-3",
                "placeholder": "Лицензияни киритинг",
            }
        ),
    )

    class Meta:
        model = models.Company
        fields = ("name", "email", "address", "phone_number", "license_number")
