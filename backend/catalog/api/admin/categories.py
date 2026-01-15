from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import status

from catalog.models import Category
from catalog.services.category_service import CategoryService
from catalog.serializers.admin.category import AdminCategorySerializer

class AdminCategoryListCreateAPIView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        categories = CategoryService().list_admin_categories()
