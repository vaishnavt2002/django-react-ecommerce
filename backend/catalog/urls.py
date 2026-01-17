from django.urls import path
from catalog.api.admin.categories import AdminCategoryListCreateAPIView, AdminCategoryUpdateAPIView
from catalog.api.admin.products import AdminProductListCreateAPIView, AdminProductUpdateAPIView
urlpatterns = [
    path("admin/categories/", AdminCategoryListCreateAPIView.as_view()),
    path("admin/category/<int:pk>/", AdminCategoryUpdateAPIView.as_view()),
    path("admin/products/", AdminProductListCreateAPIView.as_view()),
    path("admin/products/<int:pk>/", AdminProductUpdateAPIView.as_view())
]