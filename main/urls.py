from django.urls import path

from main import views

app_name = "main"

urlpatterns = [
    path("dashboard/", views.DashboardView.as_view(), name="dashboard"),
    # User
    path("users/", views.UserListView.as_view(), name="user-list"),
    path("users/create/", views.UserCreateView.as_view(), name="user-create"),
    path("users/<int:user_pk>/", views.UserUpdateView.as_view(), name="user-update"),
    # Warehouse
    path("warehouses/", views.WarehouseListView.as_view(), name="warehouse-list"),
    path("warehouses/create/", views.WarehouseCreateView.as_view(), name="warehouse-create"),
    path("warehouses/<int:warehouse_pk>/", views.WarehouseUpdateView.as_view(), name="warehouse-update"),
    # Warehouse -> Stock
    path("warehouses/<int:warehouse_pk>/stock/", views.StockListView.as_view(), name="stock-list"),
    path("warehouses/<int:warehouse_pk>/stock/create/", views.StockCreateView.as_view(), name="stock-create"),
    path("warehouses/<int:warehouse_pk>/stock/<int:stock_pk>/", views.StockUpdateView.as_view(), name="stock-update"),
    # Product
    path("products/", views.ProductListView.as_view(), name="product-list"),
    path("products/create/", views.ProductCreateView.as_view(), name="product-create"),
    path("products/<int:product_pk>/", views.ProductUpdateView.as_view(), name="product-update"),
    # Product -> Category
    path("products/categories/", views.CategoryListView.as_view(), name="category-list"),
    path("products/categories/create/", views.CategoryCreateView.as_view(), name="category-create"),
    path("products/categories/<int:category_pk>/", views.CategoryUpdateView.as_view(), name="category-update"),
]
