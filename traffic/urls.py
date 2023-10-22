from django.urls import path

from traffic import views

app_name = "traffic"

urlpatterns = [
    # Supplier
    path("suppliers/", views.SupplierListView.as_view(), name="supplier-list"),
    path("suppliers/create/", views.SupplierCreateView.as_view(), name="supplier-create"),
    path("suppliers/<int:supplier_pk>/", views.SupplierUpdateView.as_view(), name="supplier-update"),
    # Transfer
    path("transfers/", views.TransferListView.as_view(), name="transfer-list"),
    path("transfers/create/", views.TransferPreCreateView.as_view(), name="transfer-pre-create"),
    path("transfers/create/<int:warehouse_pk>/", views.TransferCreateView.as_view(), name="transfer-create"),
    path("transfers/<int:transfer_pk>/", views.TransferDetailReadView.as_view(), name="transfer-read"),
    # Order
    path("orders/", views.OrderListView.as_view(), name="order-list"),
    path("orders/create/", views.OrderPreCreateView.as_view(), name="order-pre-create"),
    path("orders/create/<int:warehouse_pk>/", views.OrderCreateView.as_view(), name="order-create"),
    path("orders/<int:order_pk>/", views.OrderDetailReadView.as_view(), name="order-read"),
    # AgentOrder
    path("agent-orders/", views.AgentOrderListView.as_view(), name="agent-order-list"),
    path("agent-orders/create/", views.AgentOrderCreateView.as_view(), name="agent-order-create"),
]
