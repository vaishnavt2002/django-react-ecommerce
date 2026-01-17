from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import status

from catalog.models import Product
from catalog.services.admin_product_service import AdminProductService
from catalog.serializers.admin.product import AdminProductSerializer

class AdminProductListCreateAPIView(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request):
        products = AdminProductService().list_admin_products()
        serializer = AdminProductSerializer(products, many=True)
        Response(serializer.data)

    def post(self, request):
        serializer = AdminProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product = AdminProductService().create_product(
            **serializer.validated_data
        )

        return Response(
            AdminProductSerializer(product).data,
            status=status.HTTP_201_CREATED
        )
class AdminProductUpdateAPIView(APIView):
    permission_classes = [IsAdminUser]

    def put(self, request, pk):
        product = Product.objects.get(pk=pk)

        serializer = AdminProductSerializer(product, data=request.data, partial=True)

        serializer.is_valid(raise_exception=True)

        product = AdminProductService().update_product(**serializer.validated_data)

        return Response(AdminProductSerializer(product).data)
    






