from django.urls import path
from catalog.api.admin.categories import (
    AdminCategoryListCreateAPIView,
    AdminCategoryUpdateAPIView
)

urlpatterns = [
    path('categories/', AdminCategoryListCreateAPIView.as_view()),
    path('categories/<int:pk>/', AdminCategoryUpdateAPIView.as_view())
]