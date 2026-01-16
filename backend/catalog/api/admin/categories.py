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
        serializer = AdminCategorySerializer(categories, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = AdminCategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        category = CategoryService().create_category(**serializer.validated_data)
        return Response(
            AdminCategorySerializer(category).data,
            status=status.HTTP_201_CREATED
        )
    
class AdminCategoryUpdateAPIView(APIView):
    permission_classes = [IsAdminUser]

    def put(self, request, pk):
        category = Category.objects.get(pk=pk)

        serializer = AdminCategorySerializer(category, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        CategoryService().update_category(
            category=category,
            **serializer.validated_data
        )

        return Response(AdminCategorySerializer(category).data)
    


