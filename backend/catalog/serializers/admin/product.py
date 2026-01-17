from rest_framework import serializers
from catalog.models import Product

class AdminProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "category",
            "gender",
            "is_active",
        ]
        read_only_fields = ("id", "is_active")
