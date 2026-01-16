from django.db import models
from .product import Product

class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="images"
    )

    color = models.CharField(
        max_length=30,
        null=True,
        blank=True
    )

    image = models.ImageField(upload_to="products/")
    is_primary = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]



