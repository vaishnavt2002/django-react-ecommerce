from rest_framework import serializers
from catalog.models import Category

class AdminCategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["name", "parent"]