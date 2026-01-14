from django.db import models
from catalog.models.product import Product

class ProductVariant(models.Model):
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE,
        related_name="variants"
    )
    size = models.CharField(max_length=20, db_index=True)
    color = models.CharField(max_length=30, db_index=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ("product", "size", "color")

    def __str__(self):
        return f"{self.product.name} - {self.size} - {self.color}"
    

