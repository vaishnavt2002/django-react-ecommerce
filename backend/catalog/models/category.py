from django.db import models
from django.core.exceptions import ValidationError
from django.db.models.functions import Lower
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children",
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Categories"
        constraints = [models.UniqueConstraint(
            Lower("name"),
            "parent",
            name="unique_category_name_per_parent_case_insensitive"
        )]

    def is_leaf(self) -> bool:
        return not self.children.exists()
    
    def clean(self):
        if self.parent and self.parent == self:
            raise ValidationError({"parent": "Category cannot be its own parent"})
        
        parent = self.parent
        while parent:
            if parent == self:
                raise ValidationError({"parent": "Circular hierarchy detected"})
            parent = parent.parent


    def __str__(self):
        return self.name
    

