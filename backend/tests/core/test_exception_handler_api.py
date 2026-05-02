import pytest
from rest_framework import status
from catalog.models.category import Category


@pytest.mark.django_db
class TestErrorEnvelopShape:
    def test_envelop_shape_is_strict(self, admin_client):
        response = admin_client.post("/api/admin/categories/", {}, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert set(response.data.keys()) == {"error"}
        assert set(response.data["error"].keys()) == {"code", "message", "details"}

    
@pytest.mark.django_db
class TestStableErrorCodes:
    def test_validation_failure_uses_validation_failed(self, admin_client):
        response = admin_client.post("/api/admin/categories/", {}, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["error"]["code"] == "validation_failed"
        assert response.data["error"]["details"] is not None

    def test_duplicate_uses_category_name_taken_and_409(self, admin_client):
        Category.objects.create(name="Books", slug="books")
        response = admin_client.post(
            "/api/admin/categories/",
            {"name": "Books"},
            format="json",
        )

        assert response.status_code == status.HTTP_409_CONFLICT
        assert response.data["error"]["code"] == "category_name_taken"

    def test_missing_resource_uses_category_not_found_and_404(self, admin_client):
        response = admin_client.put(
            "/api/admin/categories/99999/",
            {"name": "X"},
            format="json",
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data["error"]["code"] == "category_not_found"

    def test_unauthenticated_uses_not_authenticated(self, api_client):
        response = api_client.get("/api/admin/categories/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"]["code"] == "not_authenticated"

@pytest.mark.django_db
class TestUnhandledExceptionPath:
    def test_unexpected_exception_returns_envelope(self, admin_client, monkeypatch):
        from catalog.services.category_service import CategoryService

        def boom(self):
            raise ValueError("internal_secret_value")
        
        monkeypatch.setattr(CategoryService, "get_category_tree", boom)

        response = admin_client.get("/api/admin/categories/")

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert response.data["error"]["code"] == "internal_error"
        assert "internal_secret_value" not in str(response.data)
