from django.urls import path
from catalog.api.admin.categories import AdminCategoryListCreateAPIView, AdminCategoryUpdateAPIView
urlpatterns = [
    path("admin/categories/", AdminCategoryListCreateAPIView.as_view()),
    path("admin/category/<int:pk>/", AdminCategoryUpdateAPIView.as_view())
]