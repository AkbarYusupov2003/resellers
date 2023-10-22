from django import forms

from main.models import Stock, Warehouse, ProductCategory
from traffic import models


class SupplierForm(forms.ModelForm):
    name = forms.CharField(
        label="Ф.И.Ш",
        max_length=255,
        widget=forms.TextInput(
            attrs={
                "class": "form-control mb-3",
                "placeholder": "Ф.И.Шни киритинг",
            }
        ),
    )
    address = forms.CharField(
        label="Адрес",
        max_length=255,
        widget=forms.TextInput(
            attrs={
                "class": "form-control mb-3",
                "placeholder": "Адресни киритинг",
            }
        ),
    )
    phone_number = forms.CharField(
        label="Телефон Раками",
        max_length=255,
        widget=forms.TextInput(
            attrs={
                "class": "form-control mb-3",
                "placeholder": "Телефон ракамини киритинг",
            }
        ),
    )
    email = forms.EmailField(
        label="Почта",
        max_length=255,
        widget=forms.EmailInput(
            attrs={
                "class": "form-control mb-3",
                "placeholder": "Почтани киритинг",
            }
        ),
        required=False
    )

    class Meta:
        model = models.Supplier
        fields = ("name", "address", "phone_number", "email")


class TransferForm(forms.ModelForm):
    destination = forms.ModelChoiceField(
        label="Кабул килувчи склад",
        queryset=Warehouse.objects.all(),
        widget=forms.Select(
            attrs={"class": "form-control mb-3"}
        )
    )
    info = forms.CharField(
        label="Тавсиф",
        max_length=1024,
        widget=forms.Textarea(
            attrs={
                "class": "form-control mb-3",
                "placeholder": "Тавсифни киритинг",
                "rows": "3"
            }
        ),
    )
    stocks = forms.ModelMultipleChoiceField(
        label="Махсулотлар",
        queryset=Stock.objects.all(),
        widget=forms.SelectMultiple(
            attrs={
                "class": "form-control selectpicker",
                "data-selected-text-format": "count > 0",
                "data-live-search": "true"
            }
        )
    )

    class Meta:
        model = models.Transfer
        fields = ("destination", "info")


class OrderForm(forms.ModelForm):
    customer_name = forms.CharField(
        label="Мижознинг исми",
        max_length=255,
        widget=forms.TextInput(
            attrs={
                "class": "form-control mb-3",
                "placeholder": "Исмини киритинг",
            }
        ),
    )
    customer_address = forms.CharField(
        label="Мижознинг адреси",
        max_length=512,
        widget=forms.TextInput(
            attrs={
                "class": "form-control mb-3",
                "placeholder": "Адресни киритинг",
            }
        ),
    )
    customer_phone = forms.CharField(
        label="Мижознинг телефон раками",
        max_length=16,
        widget=forms.TextInput(
            attrs={
                "class": "form-control mb-3",
                "placeholder": "Телефон ракамини киритинг",
            }
        ),
    )
    stocks = forms.ModelMultipleChoiceField(
        label="Махсулотлар",
        queryset=Stock.objects.all(),
        widget=forms.SelectMultiple(
            attrs={
                "class": "form-control selectpicker",
                "data-selected-text-format": "count > 0",
                "data-live-search": "true"
            }
        )
    )

    class Meta:
        model = models.Order
        fields = ("customer_name", "customer_address", "customer_phone")


class AgentOrder(forms.ModelForm):
    # forms.ModelChoiceField(
    #         label="Кабул килувчи склад",
    #         queryset=Warehouse.objects.all(),
    #         widget=forms.Select(
    #             attrs={"class": "form-control mb-3"}
    #         )
    #     )
    supplier = forms.ModelChoiceField(
        label="Мижоз",
        queryset=models.Supplier.objects.all(),
        widget=forms.Select(
            attrs={"class": "form-control mb-3"}
        )
    )
    product_category = forms.ModelChoiceField(
        label="Махсулотлар гурухи",
        queryset=ProductCategory.objects.all(),
        widget=forms.Select(
            attrs={"class": "form-control mb-3"}
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
    class Meta:
        model = models.AgentOrder
        fields = ("supplier", "product_category", "description")
