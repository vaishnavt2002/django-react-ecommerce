from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from catalog.models import Category
from catalog.services.category_service import CategoryService
from catalog.serializers.admin.category import AdminCategoryCreateSerializer, AdminCategoryUpdateSerializer
from ecommerce.core.logging import get_logger
from django.core.exceptions import ValidationError

logger = get_logger(__name__)

class AdminCategoryListCreateAPIView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        logger.info("admin_category_list_api_called")
        tree = CategoryService().get_category_tree()

        logger.info(
            "admin_category_list_api_success",
            total_roots=len(tree)
        )

        return Response(tree)
    
    def post(self, request):
        logger.info("admin_category_create_api_called")

        serializer = AdminCategoryCreateSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        category = CategoryService().create_category(
            **serializer.validated_data
        )

        logger.info(
            "admin_category_create_api_success",
            category_id=category.id,
            slug=category.slug
        )

        return Response(
            AdminCategoryCreateSerializer(category).data,
            status=status.HTTP_201_CREATED
        )
    
class AdminCategoryUpdateAPIView(APIView):
    permission_classes = [IsAdminUser]

    def put(self, request, pk):
        logger.info(
            "admin_category_update_api_called",
            category_id=pk
        )

        category = CategoryService().get_category_by_id(pk=pk)
        
        serializer = AdminCategoryUpdateSerializer(
            category,
            data=request.data,
            partial=True
        )

        serializer.is_valid(raise_exception=True)


        updated_category = CategoryService().update_category(
            category=category,
            **serializer.validated_data
        )

        logger.info(
            "admin_category_update_api_success",
            category_id=category.id
        )

        return Response(
            AdminCategoryUpdateSerializer(updated_category).data
        )
