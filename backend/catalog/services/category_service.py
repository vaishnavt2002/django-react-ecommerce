from catalog.models import Category

class CategoryService:

    def create_category(self, *, name, slug, parent=None):
        category = Category(
            name=name,
            slug=slug,
            parent=parent,
        )

        category.full_clean()
        category.save()
        return category
    
    def update_category(self, *, category, **data):
        for field, value in data.items():
            setattr(category, field, value)
        category.full_clean()
        category.save()
        return category
    
    def disable_category(self, *, category):
        category.is_active= False
        category.save(update_fields=["is_active"])
        return category
    
    def list_admin_categories(self):
        return Category.objects.all().select_related("parent")

