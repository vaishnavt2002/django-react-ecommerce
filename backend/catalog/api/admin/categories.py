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
        try:
            tree = CategoryService().get_category_tree()

            logger.info(
                "admin_category_list_api_success",
                total_roots=len(tree)
            )

            return Response(tree)

        except Exception as e:
            logger.error(
                "admin_category_list_api_system_error",
                error=str(e),
                exc_info=True
            )
            return Response(
                {"error": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def post(self, request):
        logger.info("admin_category_create_api_called")

        serializer = AdminCategoryCreateSerializer(data=request.data)

        if not serializer.is_valid():
            logger.warning(
                "admin_category_create_validation_failed",
                errors=serializer.errors
            )
            return Response(serializer.errors, status=400)

        try:
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

        except ValidationError as e:
            logger.warning(
                "admin_category_create_business_error",
                error=str(e)
            )
            return Response(
                e.message_dict if hasattr(e, "message_dict") else {"error": e.detail},
                status=status.HTTP_400_BAD_REQUEST
            )

        except Exception as e:
            logger.error(
                "admin_category_create_api_system_error",
                error=str(e),
                exc_info=True
            )
            return Response(
                {"error": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
class AdminCategoryUpdateAPIView(APIView):
    permission_classes = [IsAdminUser]

    def put(self, request, pk):
        logger.info(
            "admin_category_update_api_called",
            category_id=pk
        )

        category = CategoryService().get_category_by_id(pk=pk)

        if category is None:
            return Response({"error": "Category not found"}, status=404)

        serializer = AdminCategoryUpdateSerializer(
            category,
            data=request.data,
            partial=True
        )

        if not serializer.is_valid():
            logger.warning(
                "admin_category_update_validation_failed",
                category_id=pk,
                errors=serializer.errors
            )
            return Response(serializer.errors, status=400)

        try:
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

        except ValidationError as e:
            logger.warning(
                "admin_category_update_business_error",
                category_id=pk,
                error=str(e)
            )
            return Response(
                e.message_dict if hasattr(e, "message_dict") else {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

        except Exception as e:
            logger.error(
                "admin_category_update_api_system_error",
                category_id=pk,
                error=str(e),
                exc_info=True
            )
            return Response(
                {"error": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    


