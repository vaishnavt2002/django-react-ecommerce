from catalog.models import Category
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from ecommerce.core.exceptions import ResourceNotFound, DuplicateResource
from django.db import transaction

class CategoryService:

    def _validate_unique_name(self, *, name, parent, exclude_id = None):
        qs = Category.objects.filter(
            parent=parent,
            name__iexact=name
        )

        if exclude_id:
            qs = qs.exclude(id=exclude_id)
        
        if qs.exists():
            raise DuplicateResource(
                detail={"name": "A category with this name already exists under this parent."},
                code="category_name_taken",
            )
    
    def _get_unique_slug(self, *, name):
        base_slug = slugify(name)
        slug = base_slug
        counter = 1
        while Category.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        return slug
    
    @transaction.atomic
    def create_category(self, *, name, parent=None):
        self._validate_unique_name(name=name, parent=parent)
        slug = self._get_unique_slug(name=name)
        category = Category(
            name=name,
            slug=slug,
            parent=parent,
        )

        category.full_clean()
        category.save()
        return category
    

    @transaction.atomic
    def update_category(self, *, category, **data):
        name = data.get("name", category.name)
        parent = data.get("parent", category.parent)

        self._validate_unique_name(
            name=name,
            parent=parent,
            exclude_id=category.id
        )

        if name != category.name:
            data["slug"] = self._get_unique_slug(name=name)
        for field, value in data.items():
            setattr(category, field, value)
        category.full_clean()
        category.save()
        return category
    
    @transaction.atomic
    def disable_category(self, *, category):
        category.is_active= False
        category.save(update_fields=["is_active"])
        return category
    
    def get_category_tree(self):
        categories = Category.objects.all().select_related("parent")
        return self._build_tree(categories)

    def _build_tree(self, categories):
        category_map = {cat.id: {"id": cat.id,
                                 "name": cat.name,
                                 "slug": cat.slug,
                                 "is_active": cat.is_active,
                                 "children": []}
                        for cat in categories}
        
        root_nodes = []

        for cat in categories:
            if cat.parent_id and cat.parent_id in category_map:
                category_map[cat.parent_id]["children"].append(category_map[cat.id])
            else:
                root_nodes.append(category_map[cat.id])

        return root_nodes
    
    def get_category_by_id(self, *, pk):
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            raise ResourceNotFound(
                detail="Category not found.",
                code="category_not_found",
            )


