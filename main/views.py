import json

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Count
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View, generic
from django.views.decorators.csrf import csrf_exempt

from main import models
from main import forms
from company.models import Company


class DashboardView(LoginRequiredMixin, generic.DetailView):
    template_name = "main/dashboard/main.html"
    model = Company

    def get(self, request, *args, **kwargs):
        company = self.get_object()
        if request.user in company.admins.all():
            return render(request, self.template_name, {"company": company})
        elif request.user in company.agents.all():
            return redirect("traffic:agent-order-list", company.pk)
        else:
            return redirect("company:list")


# User
class UserListView(LoginRequiredMixin, generic.ListView):
    template_name = "main/user/list.html"
    model = get_user_model()
    paginate_by = 10

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        company = get_object_or_404(Company, pk=kwargs["pk"])
        if request.user in company.admins.all():
            self.object_list = self.get_queryset()
            return render(
                request,
                self.template_name,
                {
                    "company": company,
                    **self.get_context_data(),
                }
            )
        else:
            return redirect("main:dashboard", pk=company.pk)

    def delete(self, request, *args, **kwargs):
        body = json.loads(request.body)
        user_pk = body.get("user_pk")
        company = get_object_or_404(Company, pk=kwargs["pk"])
        if request.user in company.admins.all():
            if str(user_pk).isdigit():
                try:
                    user = get_user_model().objects.get(pk=user_pk)
                    if user in company.admins.all():
                        company.admins.remove(user)
                    if user in company.agents.all():
                        company.agents.remove(user)
                    return HttpResponse(status=200)
                except:
                    pass
        return HttpResponse(status=403)

    def get_queryset(self):
        company = get_object_or_404(Company, pk=self.kwargs["pk"])
        return company.admins.all().union(
            company.agents.all()
        ).order_by("-pk")


class UserCreateView(LoginRequiredMixin, generic.DetailView):
    template_name = "main/user/create.html"
    model = models.Company
    form_class = forms.UserCreateForm

    def get(self, request, *args, **kwargs):
        company = self.get_object()
        if request.user in company.admins.all():
            return render(
                request,
                self.template_name,
                {"company": company, "form": self.form_class}
            )
        else:
            return redirect("main:dashboard", pk=company.pk)

    def post(self, request, *args, **kwargs):
        company = self.get_object()
        if request.user in company.admins.all():
            form = self.form_class(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.set_password(form.cleaned_data["password"])
                user.save()
                if form.cleaned_data["role"] == "ADMIN":
                    company.admins.add(user)
                elif form.cleaned_data["role"] == "AGENT":
                    company.agents.add(user)
                messages.success(request, "Янги фойдаланувчи яратилди")
                return redirect("main:user-list", pk=company.pk)
            else:
                return render(
                    request,
                    self.template_name,
                    {"company": company, "form": form}
                )
        else:
            return redirect("main:dashboard", pk=company.pk)


class UserUpdateView(LoginRequiredMixin, generic.DetailView):
    template_name = "main/user/update.html"
    model = models.Company
    form_class = forms.UserUpdateForm

    def get(self, request, *args, **kwargs):
        company = self.get_object()
        if request.user in company.admins.all():
            user = get_user_model().objects.filter(
                pk=kwargs["user_pk"]
            ).first()

            if user in company.admins.all():
                form = self.form_class(
                    instance=user, initial={"role": "ADMIN"}
                )
                return render(
                    request,
                    self.template_name,
                    {"company": company, "form": form}
                )

            elif user in company.agents.all():
                form = self.form_class(
                    instance=user, initial={"role": "AGENT"}
                )
                return render(
                    request,
                    self.template_name,
                    {"company": company, "form": form}
                )

        return redirect("main:dashboard", pk=company.pk)

    def post(self, request, *args, **kwargs):
        company = self.get_object()
        if request.user in company.admins.all():
            user = get_user_model().objects.filter(
                pk=kwargs["user_pk"]
            ).first()
            role = request.POST["role"]
            if role == "ADMIN":
                if user in company.agents.all():
                    company.agents.remove(user)
                    company.admins.add(user)

                messages.success(request, "Фойдаланувчи узгартирилди")
                return redirect("main:user-list", pk=company.pk)

            elif role == "AGENT":
                if user in company.admins.all():
                    company.admins.remove(user)
                    company.agents.add(user)

                messages.success(request, "Фойдаланувчи узгартирилди")
                return redirect("main:user-list", pk=company.pk)

        return redirect("main:dashboard", pk=company.pk)


# Warehouse
class WarehouseListView(LoginRequiredMixin, generic.DetailView):
    template_name = "main/warehouse/list.html"
    model = models.Company

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        # TODO CHANGE FOR WAREHOUSEMAN (склад, перемещение, буюртмалар)
        company = self.get_object()
        if request.user in company.admins.all():
            warehouses = company.warehouses.all().annotate(
                users_count=Count("users")
            )
            return render(
                request,
                self.template_name,
                {"company": company, "warehouses": warehouses}
            )

        return redirect("main:dashboard", pk=company.pk)

    def delete(self, request, *args, **kwargs):
        body = json.loads(request.body)
        warehouse_pk = body.get("warehouse_pk")
        company = self.get_object()
        if request.user in company.admins.all():
            if str(warehouse_pk).isdigit():
                try:
                    models.Warehouse.objects.get(
                        owner=company, pk=warehouse_pk
                    ).delete()
                    return HttpResponse(status=200)
                except:
                    pass
        return HttpResponse(status=403)


class WarehouseCreateView(LoginRequiredMixin, generic.DetailView):
    template_name = "main/warehouse/create.html"
    model = models.Company
    form_class = forms.WarehouseForm

    def get(self, request, *args, **kwargs):
        company = self.get_object()
        if request.user in company.admins.all():
            form = self.form_class()
            return render(
                request,
                self.template_name,
                {"company": company, "form": form}
            )
        else:
            return redirect("main:dashboard", pk=company.pk)

    def post(self, request, *args, **kwargs):
        company = self.get_object()
        if request.user in company.admins.all():
            form = self.form_class(request.POST)
            if form.is_valid():
                warehouse = form.save(commit=False)
                warehouse.owner = company
                warehouse.save()
                messages.success(request, "Янги склад яратилди")
                return redirect("main:warehouse-list", pk=company.pk)
            else:
                return render(
                    request,
                    self.template_name,
                    {"company": company, "form": form}
                )
        else:
            return redirect("main:dashboard", pk=company.pk)


class WarehouseUpdateView(LoginRequiredMixin, generic.DetailView):
    template_name = "main/warehouse/update.html"
    model = models.Company
    form_class = forms.WarehouseForm

    def get(self, request, *args, **kwargs):
        company = self.get_object()
        if request.user in company.admins.all():
            warehouse = models.Warehouse.objects.filter(
                owner=company, pk=kwargs["warehouse_pk"]
            ).first()
            if warehouse:
                form = self.form_class(instance=warehouse)
                return render(
                    request,
                    self.template_name,
                    {"company": company, "form": form}
                )

        return redirect("main:dashboard", pk=company.pk)

    def post(self, request, *args, **kwargs):
        company = self.get_object()
        if request.user in company.admins.all():
            warehouse = models.Warehouse.objects.filter(
                owner=company, pk=kwargs["warehouse_pk"]
            ).first()
            if warehouse:
                form = self.form_class(request.POST, instance=warehouse)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Склад узгартирилди")
                    return redirect("main:warehouse-list", pk=company.pk)
                else:
                    return render(
                        request,
                        self.template_name,
                        {"company": company, "form": form}
                    )

        return redirect("main:dashboard", pk=company.pk)


# Warehouse -> Stock
class StockListView(LoginRequiredMixin, generic.ListView):
    template_name = "main/warehouse/stock/list.html"
    model = models.Stock
    paginate_by = 10

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        company = get_object_or_404(Company, pk=kwargs["pk"])
        if request.user in company.admins.all():
            warehouse = models.Warehouse.objects.filter(
                owner=company, pk=kwargs["warehouse_pk"]
            ).first()
            if warehouse:
                self.object_list = self.get_queryset()
                filter_categories = models.ProductCategory.objects.filter(
                    owner=company
                )

                name = request.GET.get("name")
                category = request.GET.get("category")

                if name:
                    messages.success(
                        request, "Махсулот номи буйича фильтр ишлатилди"
                    )
                    self.object_list = self.object_list.filter(product__name__icontains=name)

                if category:
                    self.object_list = self.object_list.filter(product__category__pk=category)
                    messages.success(
                        request, f"Махсулот гурухи буйича фильтр ишлатилди"
                    )

                return render(
                    request,
                    self.template_name,
                    {
                        "company": company,
                        "warehouse": warehouse,
                        "filter_categories": filter_categories,
                        **self.get_context_data(),
                    }
                )

        return redirect("main:dashboard", pk=company.pk)

    def delete(self, request, *args, **kwargs):
        body = json.loads(request.body)
        stock_pk = body.get("stock_pk")
        company = get_object_or_404(Company, pk=kwargs["pk"])
        if request.user in company.admins.all():
            if str(stock_pk).isdigit():
                try:
                    warehouse = models.Warehouse.objects.get(
                        owner=company, pk=kwargs["warehouse_pk"]
                    )
                    models.Stock.objects.get(
                        warehouse=warehouse, pk=stock_pk
                    ).delete()
                    return HttpResponse(status=200)
                except:
                    pass
        return HttpResponse(status=403)

    def get_queryset(self):
        warehouse = models.Warehouse.objects.filter(
            owner__pk=self.kwargs["pk"], pk=self.kwargs["warehouse_pk"]
        ).first()
        return models.Stock.objects.filter(
            warehouse=warehouse
        ).select_related("product").order_by("-pk")


class StockCreateView(LoginRequiredMixin, generic.DetailView):
    template_name = "main/warehouse/stock/create.html"
    model = models.Company
    form_class = forms.StockForm

    def get(self, request, *args, **kwargs):
        company = self.get_object()
        if request.user in company.admins.all():
            warehouse = models.Warehouse.objects.filter(
                owner=company, pk=kwargs["warehouse_pk"]
            ).first()
            if warehouse:
                form = self.form_class()
                form.fields["product"].queryset = models.Product.objects.filter(supplier__owner=company)
                return render(
                    request,
                    self.template_name,
                    {"company": company, "warehouse": warehouse, "form": form}
                )

        return redirect("main:dashboard", pk=company.pk)

    def post(self, request, *args, **kwargs):
        company = self.get_object()
        if request.user in company.admins.all():
            warehouse = models.Warehouse.objects.filter(
                owner=company, pk=kwargs["warehouse_pk"]
            ).first()
            if warehouse:
                form = self.form_class(request.POST)
                if form.is_valid():
                    stock = form.save(commit=False)
                    stock.warehouse = warehouse
                    stock.save()
                    messages.success(request, "Янги мавжуд махсулот яратилди")
                    return redirect(
                        "main:stock-list",
                        pk=company.pk, warehouse_pk=warehouse.pk
                    )
                else:
                    return render(
                        request,
                        self.template_name,
                        {
                            "company": company,
                            "warehouse": warehouse,
                            "form": form
                        }
                    )

        return redirect("main:dashboard", pk=company.pk)


class StockUpdateView(LoginRequiredMixin, generic.DetailView):
    template_name = "main/warehouse/stock/update.html"
    model = models.Company
    form_class = forms.StockForm

    def get(self, request, *args, **kwargs):
        company = self.get_object()
        if request.user in company.admins.all():
            warehouse = models.Warehouse.objects.filter(
                owner=company, pk=kwargs["warehouse_pk"]
            ).first()
            if warehouse:
                stock = models.Stock.objects.filter(
                    warehouse=warehouse, pk=kwargs["stock_pk"]
                ).first()
                if stock:
                    form = self.form_class(instance=stock)
                    form.fields["product"].queryset = models.Product.objects.filter(supplier__owner=company)
                    return render(
                        request,
                        self.template_name,
                        {
                            "company": company,
                            "warehouse": warehouse,
                            "form": form
                        }
                    )
        return redirect("main:dashboard", pk=company.pk)

    def post(self, request, *args, **kwargs):
        company = self.get_object()
        if request.user in company.admins.all():
            warehouse = models.Warehouse.objects.filter(
                owner=company, pk=kwargs["warehouse_pk"]
            ).first()
            if warehouse:
                stock = models.Stock.objects.filter(
                    warehouse=warehouse, pk=kwargs["stock_pk"]
                ).first()
                if stock:
                    form = self.form_class(request.POST, instance=stock)
                    if form.is_valid():
                        form.save()
                        messages.success(request, "Мавжуд махсулот узгартирилди")
                        return redirect(
                            "main:stock-list",
                            pk=company.pk, warehouse_pk=warehouse.pk
                        )
                    else:
                        return render(
                            request,
                            self.template_name,
                            {
                                "company": company,
                                "warehouse": warehouse,
                                "form": form
                            }
                        )

        return redirect("main:dashboard", pk=company.pk)


# Product
class ProductListView(LoginRequiredMixin, generic.ListView):
    template_name = "main/product/list.html"
    model = models.Product
    paginate_by = 10

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        company = get_object_or_404(Company, pk=kwargs["pk"])
        if request.user in company.admins.all():
            self.object_list = self.get_queryset()
            filter_categories = models.ProductCategory.objects.filter(
                owner=company
            )

            name = request.GET.get("name")
            category = request.GET.get("category")

            if name:
                messages.success(
                    request, "Махсулот номи буйича фильтр ишлатилди"
                )
                self.object_list = self.object_list.filter(name__icontains=name)

            if category:
                self.object_list = self.object_list.filter(category__pk=category)
                messages.success(
                    request, f"Махсулот гурухи буйича фильтр ишлатилди"
                )

            return render(
                request,
                self.template_name,
                {
                    "company": company,

                    "filter_categories": filter_categories,
                    **self.get_context_data()
                }
            )
        else:
            return redirect("main:dashboard", pk=company.pk)

    def delete(self, request, *args, **kwargs):
        body = json.loads(request.body)
        product_pk = body.get("product_pk")
        company = get_object_or_404(Company, pk=kwargs["pk"])
        if request.user in company.admins.all():
            if str(product_pk).isdigit():
                try:
                    models.Product.objects.get(
                        supplier__owner=company, pk=product_pk
                    ).delete()
                    return HttpResponse(status=200)
                except:
                    pass
        return HttpResponse(status=403)

    def get_queryset(self):
        company = get_object_or_404(Company, pk=self.kwargs["pk"])
        return models.Product.objects.filter(
            supplier__owner=company
        ).select_related("supplier", "category").order_by("-pk")


class ProductCreateView(LoginRequiredMixin, generic.DetailView):
    template_name = "main/product/create.html"
    model = models.Company
    form_class = forms.ProductForm

    def get(self, request, *args, **kwargs):
        company = self.get_object()
        if request.user in company.admins.all():
            form = self.form_class
            return render(
                request,
                self.template_name,
                {"company": company, "form": form}
            )
        else:
            return redirect("main:dashboard", pk=company.pk)

    def post(self, request, *args, **kwargs):
        company = self.get_object()
        if request.user in company.admins.all():
            form = self.form_class(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Янги махсулот яратилди")
                return redirect("main:product-list", pk=company.pk)
            else:
                return render(
                    request,
                    self.template_name,
                    {"company": company, "form": form}
                )
        else:
            return redirect("main:dashboard", pk=company.pk)


class ProductUpdateView(LoginRequiredMixin, generic.DetailView):
    template_name = "main/product/update.html"
    model = models.Company
    form_class = forms.ProductForm

    def get(self, request, *args, **kwargs):
        company = self.get_object()
        if request.user in company.admins.all():
            product = models.Product.objects.filter(
                supplier__owner=company, pk=kwargs["product_pk"]
            ).first()
            if product:
                form = self.form_class(instance=product)
                return render(
                    request,
                    self.template_name,
                    {"company": company, "form": form}
                )

        return redirect("main:dashboard", pk=company.pk)

    def post(self, request, *args, **kwargs):
        company = self.get_object()
        if request.user in company.admins.all():
            product = models.Product.objects.filter(
                supplier__owner=company, pk=kwargs["product_pk"]
            ).first()
            if product:
                form = self.form_class(request.POST, instance=product)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Махсулот узгартирилди")
                    return redirect("main:product-list", pk=company.pk)
                else:
                    return render(
                        request,
                        self.template_name,
                        {"company": company, "form": form}
                    )

        return redirect("main:dashboard", pk=company.pk)


# Category
class CategoryListView(LoginRequiredMixin, generic.ListView):
    template_name = "main/product/category/list.html"
    model = models.ProductCategory
    paginate_by = 10

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        company = get_object_or_404(Company, pk=kwargs["pk"])
        if request.user in company.admins.all():
            self.object_list = self.get_queryset()
            return render(
                request,
                self.template_name,
                {"company": company, **self.get_context_data()}
            )
        else:
            return redirect("main:dashboard", pk=company.pk)

    def delete(self, request, *args, **kwargs):
        body = json.loads(request.body)
        category_pk = body.get("category_pk")
        company = get_object_or_404(Company, pk=kwargs["pk"])
        if request.user in company.admins.all():
            if str(category_pk).isdigit():
                try:
                    models.ProductCategory.objects.get(
                        owner=company, pk=category_pk
                    ).delete()
                    return HttpResponse(status=200)
                except:
                    pass
        return HttpResponse(status=403)

    def get_queryset(self):
        return models.ProductCategory.objects.filter(
            owner__pk=self.kwargs["pk"]
        ).order_by("-pk")


class CategoryCreateView(LoginRequiredMixin, generic.DetailView):
    template_name = "main/product/category/create.html"
    model = models.Company
    form_class = forms.CategoryForm

    def get(self, request, *args, **kwargs):
        company = self.get_object()
        if request.user in company.admins.all():
            form = self.form_class
            return render(
                request, self.template_name, {"company": company, "form": form}
            )
        else:
            return redirect("main:dashboard", pk=company.pk)

    def post(self, request, *args, **kwargs):
        company = self.get_object()
        if request.user in company.admins.all():
            form = self.form_class(request.POST)
            if form.is_valid():
                category = form.save(commit=False)
                category.owner = company
                category.save()
                messages.success(request, "Янги гурух яратилди")
                return redirect("main:category-list", pk=company.pk)
            else:
                return render(
                    request,
                    self.template_name,
                    {"company": company, "form": form}
                )
        else:
            return redirect("main:dashboard", pk=company.pk)


class CategoryUpdateView(LoginRequiredMixin, generic.DetailView):
    template_name = "main/product/category/update.html"
    model = models.Company
    form_class = forms.CategoryForm

    def get(self, request, *args, **kwargs):
        company = self.get_object()
        if request.user in company.admins.all():
            category = models.ProductCategory.objects.filter(
                owner=company, pk=kwargs["category_pk"]
            ).first()
            if category:
                form = self.form_class(instance=category)
                return render(
                    request, self.template_name, {"company": company, "form": form}
                )

        return redirect("main:dashboard", pk=company.pk)

    def post(self, request, *args, **kwargs):
        company = self.get_object()
        if request.user in company.admins.all():
            category = models.ProductCategory.objects.filter(
                owner=company, pk=kwargs["category_pk"]
            ).first()
            if category:
                form = self.form_class(request.POST, instance=category)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Гурух узгартирилди")
                    return redirect("main:category-list", pk=company.pk)
                else:
                    return render(
                        request,
                        self.template_name,
                        {"company": company, "form": form}
                    )

        return redirect("main:dashboard", pk=company.pk)
