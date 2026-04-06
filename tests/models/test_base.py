from app.models.base import BaseModel


class TestBaseModel:
    def test_abstract(self):
        assert BaseModel.__abstract__ is True

    def test_has_id_column(self):
        assert hasattr(BaseModel, "id")

    def test_has_timestamps(self):
        assert hasattr(BaseModel, "created_at")
        assert hasattr(BaseModel, "updated_at")

    def test_has_is_active(self):
        assert hasattr(BaseModel, "is_active")

    def test_has_save_method(self):
        assert hasattr(BaseModel, "save")

    def test_has_delete_method(self):
        assert hasattr(BaseModel, "delete")

    def test_has_update_method(self):
        assert hasattr(BaseModel, "update")
