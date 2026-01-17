from catalog.models import Category
from catalog.models import Product
class AdminProductService:
    def create_product(self, *, name: str, slug: str, category: Category, gender: str, description: str = "" ) -> Product:
        product = Product(
            name=name,
            slug=slug,
            category=category,
            gender=gender,
            description=description,
            is_active=False
        )

        product.save()
        return product
    
    def update_product(self, *, product: Product, **data)-> Product:
        for field, value in data.items():
            setattr(product, field, value)
        
        product.save()
        return product
    
    def disable_product(self, *, product: Product) -> None:
        product.is_active = False
        product.save(update_fields=["is_active"])
    
    def list_admin_products(self):
        return Product.objects.select_related("category").all()
    
    



