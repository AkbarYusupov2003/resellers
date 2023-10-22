from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View

from accounts import forms


class RegisterView(View):
    template_name = "accounts/auth/register.html"
    form_class = forms.RegistrationForm

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {"form": self.form_class})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()
            login(request, user)
            return redirect("company:list")

        return render(request, self.template_name, {"form": form})


class LoginView(View):
    template_name = "accounts/auth/login.html"
    form_class = forms.LoginForm

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {"form": self.form_class})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect("company:list")
            else:
                messages.error(request, "login error")

        return render(request, self.template_name, {"form": form})


class EditAccountView(View):
    template_name = "accounts/edit.html"
    form_class = forms.EditAccountForm

    def get(self, request, *args, **kwargs):
        form = self.form_class(instance=self.request.user)
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, instance=self.request.user)
        if form.is_valid():
            form.save()

        return redirect("company:list")
