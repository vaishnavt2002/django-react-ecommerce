import pytest
from catalog.services.category_service import CategoryService
from ecommerce.core.exceptions import DuplicateResource, ResourceNotFound
from catalog.models import Category


@pytest.fixture
def service():
    return CategoryService()

@pytest.fixture
def root_category(service):
    return service.create_category(name="Men")

@pytest.mark.django_db
class TestCreateCategory:
    def test_creates_root_category(self, service):
        category = service.create_category(name="Men")

        assert category.id is not None
        assert category.name == "Men"
        assert category.slug == "men"
        assert category.parent is None
        assert category.is_active is True

    def test_creates_child_category(self, service, root_category):
        child = service.create_category(
            name="Women",
            parent=root_category
        )

        assert child.parent == root_category
        assert child.slug == "women"

    def test_generates_unique_slug_on_collision(self, service):
        service.create_category(name="Shirt")
        parent = service.create_category(name="Women")

        child = service.create_category(name="Shirt", parent=parent)

        assert child.slug == "shirt-1"

    def test_rejects_duplicate_name_under_same_parent(self, service):
        service.create_category(name="Men")

        with pytest.raises(DuplicateResource) as exc_info:
            service.create_category(name="Men")

        assert "name" in exc_info.value.detail

    def test_rejects_duplicate_name_case_insensitive(self, service):
        service.create_category(name="Men")

        with pytest.raises(DuplicateResource) as exc_info:
            service.create_category(name="MEN")

    def test_allows_same_name_under_different_parents(self, service):
        parent1 = service.create_category(name="Men")
        parent2 = service.create_category(name="Women")

        shirt1 = service.create_category(name="Shirt", parent=parent1)
        shirt2 = service.create_category(name="Shirt", parent=parent2)

        assert shirt2.slug == "shirt-1"

@pytest.mark.django_db
class TestGetCategoryTree:

    def test_returns_empty_list_when_no_categories(self, service):
        tree = service.get_category_tree()
        assert tree == []

    def test_returns_flat_list_for_root_only(self, service):
        service.create_category(name="Men")
        service.create_category(name="Women")

        tree = service.get_category_tree()
        root_nodes = {node["name"] for node in tree}

        assert len(tree) == 2
        assert root_nodes == {"Men", "Women"}

    def test_nests_children_under_parents(self, service):
        men = service.create_category(name="Men")
        service.create_category(name="Shirt", parent=men)
        service.create_category(name="Pants", parent=men)
        tree = service.get_category_tree()

        assert len(tree) == 1
        assert len(tree[0]["children"]) == 2
        child_names = {child["name"] for child in tree[0]["children"]}
        assert child_names == {"Shirt", "Pants"}

    def test_builds_deep_hierarchy(self, service):
        """Three levels: Electronics > Laptops > Gaming Laptops"""
        electronics = service.create_category(name="Electronics")
        laptops = service.create_category(
            name="Laptops", parent=electronics
        )
        service.create_category(
            name="Gaming Laptops", parent=laptops
        )

        tree = service.get_category_tree()

        gaming = tree[0]["children"][0]["children"]
        assert len(gaming) == 1
        assert gaming[0]["name"] == "Gaming Laptops"