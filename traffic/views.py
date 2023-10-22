import json

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.decorators.csrf import csrf_exempt

from main.models import Company, Stock, ProductCategory

from traffic import models
from traffic import forms


# Supplier
class SupplierListView(LoginRequiredMixin, generic.ListView):
    template_name = "traffic/supplier/list.html"
    model = models.Supplier
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
            return redirect("company:list")

    def delete(self, request, *args, **kwargs):
        body = json.loads(request.body)
        supplier_pk = body.get("supplier_pk")
        company = get_object_or_404(Company, pk=kwargs["pk"])
        if request.user in company.admins.all():
            if str(supplier_pk).isdigit():
                try:
                    models.Supplier.objects.get(
                        owner=company, pk=supplier_pk
                    ).delete()
                    return HttpResponse(status=200)
                except:
                    pass
        return HttpResponse(status=403)

    def get_queryset(self):
        company = get_object_or_404(Company, pk=self.kwargs["pk"])
        return company.suppliers.all().order_by("-pk")


class SupplierCreateView(LoginRequiredMixin, generic.DetailView):
    template_name = "traffic/supplier/create.html"

    model = Company
    form_class = forms.SupplierForm

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
                supplier = form.save(commit=False)
                supplier.owner = company
                supplier.save()
                messages.success(request, "Янги етказиб берувчи яратилди")
                return redirect("traffic:supplier-list", pk=company.pk)
            else:
                return render(
                    request,
                    self.template_name,
                    {"company": company, "form": form}
                )
        else:
            return redirect("main:dashboard", pk=company.pk)


class SupplierUpdateView(LoginRequiredMixin, generic.DetailView):
    template_name = "traffic/supplier/update.html"
    model = models.Company
    form_class = forms.SupplierForm

    def get(self, request, *args, **kwargs):
        company = self.get_object()
        if request.user in company.admins.all():
            supplier = models.Supplier.objects.filter(
                owner=company, pk=kwargs["supplier_pk"]
            ).first()
            if supplier:
                form = self.form_class(instance=supplier, )
                return render(
                    request, self.template_name,
                    {"company": company, "form": form}
                )

        return redirect("main:dashboard", pk=company.pk)

    def post(self, request, *args, **kwargs):
        company = self.get_object()
        if request.user in company.admins.all():
            supplier = models.Supplier.objects.filter(
                owner=company, pk=kwargs["supplier_pk"]
            ).first()
            if supplier:
                form = self.form_class(request.POST, instance=supplier)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Етказиб берувчи узгартирилди")
                    return redirect("traffic:supplier-list", pk=company.pk)
                else:
                    return render(
                        request,
                        self.template_name,
                        {"company": company, "form": form}
                    )

        return redirect("main:dashboard", pk=company.pk)


# Transfer
class TransferListView(LoginRequiredMixin, generic.ListView):
    template_name = "traffic/transfer/list.html"
    model = models.Transfer
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        company = get_object_or_404(Company, pk=kwargs["pk"])
        if request.user in company.admins.all():
            self.object_list = self.get_queryset()
            return render(
                request, self.template_name,
                {"company": company, **self.get_context_data()}
            )

        return redirect("main:dashboard", pk=company.pk)

    def get_queryset(self):
        return models.Transfer.objects.filter(
            owner__pk=self.kwargs["pk"]
        ).select_related("source", "destination").order_by("-pk")


class TransferPreCreateView(LoginRequiredMixin, generic.DetailView):
    template_name = "traffic/transfer/pre_create.html"
    model = Company

    def get(self, request, *args, **kwargs):
        company = self.get_object()
        if request.user in company.admins.all():
            return render(
                request, self.template_name,
                {"company": company, "warehouses": company.warehouses.all()}
            )

        return redirect("main:dashboard", pk=company.pk)


class TransferCreateView(LoginRequiredMixin, generic.DetailView):
    template_name = "traffic/transfer/create.html"
    model = Company
    form_class = forms.TransferForm

    def get(self, request, *args, **kwargs):
        company = self.get_object()
        if request.user in company.admins.all():
            giving_warehouse = models.Warehouse.objects.filter(
                owner=company, pk=kwargs["warehouse_pk"]
            ).first()
            if giving_warehouse:
                form = self.form_class()
                form.fields["destination"].queryset = company.warehouses.all().exclude(pk=kwargs["warehouse_pk"])
                form.fields["stocks"].queryset = Stock.objects.filter(
                    warehouse=giving_warehouse
                ).select_related("product")

                return render(
                    request, self.template_name,
                    {
                        "company": company,
                        "giving_warehouse": giving_warehouse,
                        "form": form
                    }
                )

        return redirect("main:dashboard", pk=company.pk)

    def post(self, request, *args, **kwargs):
        company = self.get_object()
        if request.user in company.admins.all():
            giving_warehouse = models.Warehouse.objects.filter(
                owner=company, pk=kwargs["warehouse_pk"]
            ).first()
            if giving_warehouse:
                form = self.form_class(request.POST)
                if form.is_valid():
                    transfer = form.save(commit=False)
                    transfer.owner = company
                    transfer.source = giving_warehouse
                    transfer.save()
                    data = ""
                    for stock in form.cleaned_data["stocks"]:
                        qty = request.POST.get(str(stock.pk))

                        if qty.isnumeric() and int(qty) >= stock.quantity:
                            stock.warehouse = transfer.destination
                            stock.save()
                            data += f"{str(stock)}\n"

                        elif qty.isnumeric() and int(qty) > 0:
                            stock.quantity = stock.quantity - int(qty)
                            stock.save()

                            new_stock = stock
                            new_stock.quantity = int(qty)
                            new_stock.warehouse = transfer.destination
                            new_stock.pk = None
                            new_stock.save()
                            data += f"{str(new_stock)}\n"

                    transfer.data = data
                    transfer.save()

                    messages.success(request, "Янги перемещение яратилди")
                    return redirect("traffic:transfer-list", pk=company.pk)
                else:
                    return render(
                        request, self.template_name,
                        {
                            "company": company,
                            "giving_warehouse": giving_warehouse,
                            "form": form
                        }
                    )

        return redirect("main:dashboard", pk=company.pk)


class TransferDetailReadView(LoginRequiredMixin, generic.DetailView):
    template_name = "traffic/transfer/read.html"
    model = Company
    form_class = forms.TransferForm

    def get(self, request, *args, **kwargs):
        company = self.get_object()
        if request.user in company.admins.all():
            transfer = models.Transfer.objects.filter(
                owner=company, pk=kwargs["transfer_pk"]
            ).first()
            if transfer:
                return render(
                    request,
                    self.template_name,
                    {"company": company, "transfer": transfer}
                )

        return redirect("main:dashboard", pk=company.pk)


# Order
class OrderListView(LoginRequiredMixin, generic.ListView):
    template_name = "traffic/order/list.html"
    model = models.Order
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        company = get_object_or_404(Company, pk=kwargs["pk"])
        if request.user in company.admins.all():
            self.object_list = self.get_queryset()
            return render(
                request,
                self.template_name,
                {"company": company, **self.get_context_data()}
            )

    def get_queryset(self):
        return models.Order.objects.filter(
            owner__pk=self.kwargs["pk"]
        ).select_related("source").order_by("-pk")


class OrderPreCreateView(LoginRequiredMixin, generic.DetailView):
    template_name = "traffic/order/pre_create.html"
    model = Company

    def get(self, request, *args, **kwargs):
        company = self.get_object()
        if request.user in company.admins.all():
            return render(
                request, self.template_name,
                {"company": company, "warehouses": company.warehouses.all()}
            )

        return redirect("main:dashboard", pk=company.pk)


class OrderCreateView(LoginRequiredMixin, generic.DetailView):
    template_name = "traffic/order/create.html"
    model = Company
    form_class = forms.OrderForm

    def get(self, request, *args, **kwargs):
        company = self.get_object()
        if request.user in company.admins.all():
            giving_warehouse = models.Warehouse.objects.filter(
                owner=company, pk=kwargs["warehouse_pk"]
            ).first()
            if giving_warehouse:
                form = self.form_class()
                form.fields["stocks"].queryset = Stock.objects.filter(
                    warehouse=giving_warehouse
                ).select_related("product")
                return render(
                    request,
                    self.template_name,
                    {
                        "company": company,
                        "giving_warehouse": giving_warehouse,
                        "form": form
                    }
                )

        return redirect("main:dashboard", pk=company.pk)

    def post(self, request, *args, **kwargs):
        company = self.get_object()
        if request.user in company.admins.all():
            giving_warehouse = models.Warehouse.objects.filter(
                owner=company, pk=kwargs["warehouse_pk"]
            ).first()
            if giving_warehouse:
                form = self.form_class(request.POST)
                if form.is_valid():
                    order = form.save(commit=False)
                    order.owner = company
                    order.source = giving_warehouse

                    data = ""
                    for stock in form.cleaned_data["stocks"]:
                        qty = request.POST.get(str(stock.pk))

                        if qty.isnumeric() and int(qty) >= stock.quantity:
                            stock.delete()
                            data += f"{str(stock)}\n"

                        elif qty.isnumeric() and int(qty) > 0:
                            stock.quantity = stock.quantity - int(qty)
                            stock.save()
                            data += f"{stock.product.category.name}, {qty}та {stock.product.name}, {stock.purchase_price} {stock.get_currency_display()}\n"

                    order.data = data
                    order.save()

                    messages.success(request, "Янги буюртма яратилди")
                    return redirect("traffic:order-list", pk=company.pk)
                else:
                    return render(
                        request, self.template_name,
                        {
                            "company": company,
                            "giving_warehouse": giving_warehouse,
                            "form": form
                        }
                    )

        return redirect("main:dashboard", pk=company.pk)


class OrderDetailReadView(LoginRequiredMixin, generic.DetailView):
    template_name = "traffic/order/read.html"
    model = Company
    form_class = forms.OrderForm

    def get(self, request, *args, **kwargs):
        company = self.get_object()
        if request.user in company.admins.all():
            order = models.Order.objects.filter(
                owner=company, pk=kwargs["order_pk"]
            ).first()
            if order:
                return render(
                    request,
                    self.template_name,
                    {"company": company, "order": order}
                )

        return redirect("main:dashboard", pk=company.pk)


# AgentOrder
class AgentOrderListView(LoginRequiredMixin, generic.ListView):
    template_name = "traffic/agent_order/dashboard.html"
    model = models.AgentOrder
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        company = get_object_or_404(Company, pk=kwargs["pk"])
        if request.user in company.agents.all() or request.user in company.admins.all():
            self.object_list = self.get_queryset()
            return render(
                request,
                self.template_name,
                {"company": company, **self.get_context_data()}
            )

    def get_queryset(self):
        return self.model.objects.filter(
            owner__pk=self.kwargs["pk"], created_by=self.request.user
        ).select_related("supplier", "product_category").order_by("-pk")


class AgentOrderCreateView(LoginRequiredMixin, generic.DetailView):
    template_name = "traffic/agent_order/create.html"
    model = Company
    form_class = forms.AgentOrder

    def get(self, request, *args, **kwargs):
        company = self.get_object()
        if request.user in company.agents.all() or request.user in company.admins.all():
            form = self.form_class()
            form.fields["product_category"].queryset = ProductCategory.objects.filter(owner=company)
            form.fields["supplier"].queryset = models.Supplier.objects.filter(owner=company)
            return render(
                request,
                self.template_name,
                {"company": company, "form": self.form_class}
            )
        else:
            return redirect("main:dashboard", pk=company.pk)

    #     def post(self, request, *args, **kwargs):
    #         company = self.get_object()
    #         if request.user in company.admins.all():
    #             form = self.form_class(request.POST)
    #             if form.is_valid():
    #                 supplier = form.save(commit=False)
    #                 supplier.owner = company
    #                 supplier.save()
    #                 messages.success(request, "Янги етказиб берувчи яратилди")
    #                 return redirect("traffic:supplier-list", pk=company.pk)
    #             else:
    #                 return render(
    #                     request,
    #                     self.template_name,
    #                     {"company": company, "form": form}
    #                 )
    #         else:
    #             return redirect("main:dashboard", pk=company.pk)
    def post(self, request, *args, **kwargs):
        company = self.get_object()
        if request.user in company.agents.all() or request.user in company.admins.all():
            form = self.form_class(request.POST)
            if form.is_valid():
                agent_order = form.save(commit=False)
                agent_order.owner = company
                agent_order.created_by = request.user
                agent_order.save()
                messages.success(request, "Янги буюртма яратилди")
                return redirect("traffic:agent-order-list", pk=company.pk)
            else:
                return render(
                    request,
                    self.template_name,
                    {"company": company, "form": form}
                )
        else:
            return redirect("main:dashboard", pk=company.pk)
