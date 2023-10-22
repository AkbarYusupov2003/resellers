from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from company import views


app_name = "company"

urlpatterns = [
    path("", views.CompanyListView.as_view(), name="list"),
    path("company-create/", views.CompanyCreateView.as_view(), name="create"),
    path("company-update/<int:pk>/", views.CompanyDetailView.as_view(), name="details"),
    #
    path("company-delete/", csrf_exempt(views.CompanyDeleteView.as_view()), name="delete"),
    path("company-leave/", csrf_exempt(views.CompanyLeaveView.as_view()), name="leave")
]
