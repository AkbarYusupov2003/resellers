from django import forms
from django.contrib.auth import get_user_model

from main import models
from traffic.models import Supplier

RoleChoices = (
    ("ADMIN", "Админ"),
    ("AGENT", "Агент")
)


class UserCreateForm(forms.ModelForm):
    role = forms.ChoiceField(
        label="Лавозимни танланг",
        choices=RoleChoices,
        widget=forms.Select(
            attrs={
                "class": "form-control mb-4",
            }
        )
    )
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
        max_length=32,
        widget=forms.TextInput(
            attrs={
                "class": "form-control mb-3",
                "placeholder": "Исмни киритинг",
            }
        ),
    )
    last_name = forms.CharField(
        label="Фамилия",
        max_length=32,
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
                "placeholder": "Паролни киритинг",
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
            raise forms.ValidationError("Пароллар бир хил эмас")

    class Meta:
        model = get_user_model()
        fields = ("username", "first_name", "last_name")


class UserUpdateForm(forms.ModelForm):
    role = forms.ChoiceField(
        label="Лавозимни узгартиринг",
        choices=RoleChoices,
        widget=forms.Select(
            attrs={
                "class": "form-control mb-4",
            }
        )
    )
    username = forms.CharField(
        label="Логин",
        min_length=4,
        max_length=64,
        widget=forms.TextInput(
            attrs={
                "class": "form-control mb-3",
                "readonly": True
            }
        ),
    )
    first_name = forms.CharField(
        label="Исм",
        max_length=32,
        widget=forms.TextInput(
            attrs={
                "class": "form-control mb-3",
                "readonly": True
            }
        ),
    )
    last_name = forms.CharField(
        label="Фамилия",
        max_length=32,
        widget=forms.TextInput(
            attrs={
                "class": "form-control mb-3",
                "readonly": True
            }
        ),
    )

    class Meta:
        model = get_user_model()
        fields = ("username", "first_name", "last_name")


class WarehouseForm(forms.ModelForm):
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

    class Meta:
        model = models.Warehouse
        fields = ("name", "address")


class StockForm(forms.ModelForm):
    product = forms.ModelChoiceField(
        label="Махсулот",
        queryset=models.Product.objects.all(),
        widget=forms.Select(
            attrs={"class": "form-control mb-3"}
        )
    )
    purchase_price = forms.IntegerField(
        label="Келган нархи",
        min_value=1,
        max_value=1_000_000_000_000,
        widget=forms.NumberInput(
            attrs={
                "class": "form-control mb-3"
            }
        )
    )
    currency = forms.ChoiceField(
        label="Валюта",
        choices=models.Stock.CurrencyChoices.choices,
        widget=forms.Select(
            attrs={
                "class": "form-control mb-3",
            }
        )
    )
    quantity = forms.IntegerField(
        label="Микдори",
        min_value=1,
        max_value=1_000_000_000_000,
        widget=forms.NumberInput(
            attrs={
                "class": "form-control mb-3"
            }
        )
    )

    class Meta:
        model = models.Stock
        fields = ("product", "purchase_price", "currency", "quantity")


class ProductForm(forms.ModelForm):
    supplier = forms.ModelChoiceField(
        label="Етказиб берувчи",
        queryset=Supplier.objects.all(),
        widget=forms.Select(
            attrs={"class": "form-control mb-3"}
        )
    )
    name = forms.CharField(
        label="Номи",
        max_length=512,
        widget=forms.TextInput(
            attrs={
                "class": "form-control mb-3",
                "placeholder": "Номини киритинг",
            }
        )
    )
    description = forms.CharField(
        label="Тавсиф",
        max_length=1024,
        widget=forms.Textarea(
            attrs={
                "class": "form-control mb-3",
                "placeholder": "Тавсифни киритинг",
                "rows": "5"
            }
        )
    )
    category = forms.ModelChoiceField(
        queryset=models.ProductCategory.objects.all(),
        label="Гурух",
        widget=forms.Select(
            attrs={"class": "form-control mb-3"}
        )
    )

    class Meta:
        model = models.Product
        fields = ("supplier", "name", "category", "description")


class CategoryForm(forms.ModelForm):
    name = forms.CharField(
        label="Номи",
        max_length=128,
        widget=forms.TextInput(
            attrs={
                "class": "form-control mb-3",
                "placeholder": "Номини киритинг",
            }
        )
    )

    class Meta:
        model = models.ProductCategory
        fields = ("name", )
