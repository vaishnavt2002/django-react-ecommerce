from django.db import models
from catalog.models.category import Category
from django.core.exceptions import ValidationError

class Product(models.Model):
    GENDER_CHOICES = (
        ("men", "Men"),
        ("women", "Women"),
        ("unisex", "Unisex"),
    )

    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='products'
    )
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if not self.category.is_leaf():
            raise ValidationError({"category":"Product must be assigned to leaf category"})
        
    def save(self,*args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name







