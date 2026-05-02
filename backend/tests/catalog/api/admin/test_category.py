import pytest
from catalog.models.category import Category

@pytest.mark.django_db
class TestAdminCategoryList:

    def test_returns_200_with_empty_list(self, admin_client):
        response = admin_client.get("/api/admin/categories/")

        assert response.status_code == 200
        assert response.data == []
    
    def test_returns_category_tree(self, admin_client):
        parent = Category.objects.create(
            name="Men",
            slug="men"
        )
    
        Category.objects.create(
            name="Shirt",
            slug="shirt",
            parent=parent
        )

        response = admin_client.get("/api/admin/categories/")

        assert response.status_code == 200
        assert len(response.data) == 1
        assert len(response.data[0]["children"]) == 1
        assert response.data[0]["name"] == "Men"
        assert response.data[0]["children"][0]["name"] == "Shirt"

class TestAdminCategoryCreate:
    
    def test_creates_category_returns_201(self, admin_client):
        response = admin_client.post(
            "/api/admin/categories/",
            {"name":"Men"},
            format="json",
        )

        assert response.status_code == 201
        assert response.data["name"] == "Men"
        assert Category.objects.count() == 1
    
    def test_creates_child_category(self, admin_client):
        parent = Category.objects.create(
            name="Men",
            slug="men"
        )

        response = admin_client.post(
            "/api/admin/categories/",
            {"name":"Shirt", "parent": parent.id},
            format="json"
        )

        assert response.status_code == 201

    def test_rejects_missing_name(self, admin_client):

        response = admin_client.post(
            "/api/admin/categories/",
            {},
            format="json"
        )

        assert response.status_code == 400

    def test_reject_duplicate_name(self, admin_client):

        admin_client.post(
            "/api/admin/categories/",
            {"name":"Shirt"},
            format="json"
        )

        response = admin_client.post(
            "/api/admin/categories/",
            {"name":"Shirt"},
            format="json"
        )

        assert response.status_code == 409








 