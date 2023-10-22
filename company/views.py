import json

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View, generic

from company import models
from company import forms


class CompanyListView(LoginRequiredMixin, View):
    template_name = "company/list.html"
    model = models.Company

    def get(self, request, *args, **kwargs):
        admin_companies = request.user.company_admin.all().order_by("-pk")
        agent_companies = request.user.company_agents.all().order_by("-pk")
        return render(
            request,
            self.template_name,
            {
                "admin_companies": admin_companies,
                "agent_companies": agent_companies
            }
        )


class CompanyDeleteView(LoginRequiredMixin, View):
    http_method_names = ("delete", )

    def delete(self, request, *args, **kwargs):
        body = json.loads(request.body)
        pk = body.get("company_pk")
        if str(pk).isdigit():
            try:
                models.Company.objects.get(
                    pk=pk, admins__in=(request.user, )
                ).delete()
                return HttpResponse(status=200)
            except models.Company.DoesNotExist:
                return HttpResponse(status=403)
        else:
            return HttpResponse(status=403)


class CompanyLeaveView(LoginRequiredMixin, View):
    http_method_names = ("delete", )

    def delete(self, request, *args, **kwargs):
        body = json.loads(request.body)
        pk = body.get("company_pk")
        if str(pk).isdigit():
            try:
                company = models.Company.objects.get(
                    pk=pk, agents__in=(request.user, )
                )
                company.agents.remove(request.user)
                return HttpResponse(status=200)
            except:
                pass
        return HttpResponse(status=403)


class CompanyCreateView(LoginRequiredMixin, View):
    template_name = "company/create.html"
    form_class = forms.CompanyForm

    def get(self, request, *args, **kwargs):
        form = self.form_class
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            company = form.save()
            company.admins.add(request.user)
            return redirect("company:list")

        return render(request, self.template_name, {"form": form})


class CompanyDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "company/details.html"
    model = models.Company
    form_class = forms.CompanyForm

    def get(self, request, *args, **kwargs):
        company = self.get_object()
        if request.user in company.admins.all():
            form = self.form_class(instance=company)
            return render(request, self.template_name, {"form": form})
        else:
            return redirect("company:list")

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, instance=self.get_object())
        if form.is_valid():
            form.save()
            messages.success(request, "Компания узгартирилди")
            return self.get(request, *args, **kwargs)

        return render(request, self.template_name, {"form": form})
