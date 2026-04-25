from rest_framework import serializers
from catalog.models import Category

class AdminCategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["name", "parent"]

class AdminCategoryUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["name", "parent", "is_active"]