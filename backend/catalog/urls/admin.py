from django.urls import path
from catalog.api.admin.categories import (
    AdminCategoryListCreateAPIView,
)

urlpatterns = [
    path('categories/', AdminCategoryListCreateAPIView.as_view()),

]