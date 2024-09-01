import os
from unittest.mock import MagicMock, patch

from django.db.models.signals import post_delete, post_save, pre_save
from django.test import TestCase
from PIL import Image

from apps.project.specific.categories.models import AssetCategoryModel

from .models import AssetModel
from .signals import (auto_delete_asset_img_on_change,
                      auto_delete_asset_img_on_delete, optimize_image)


class AssetModelTestCase(TestCase):
    def setUp(self):
        self.category = AssetCategoryModel.objects.create(name="Category 1")
        self.asset = AssetModel.objects.create(
            name="Test Asset",
            es_name="Activo de prueba",
            category=self.category,
            total_quantity=100
        )

    def test_asset_creation(self):
        self.assertEqual(AssetModel.objects.count(), 1)
        self.assertEqual(self.asset.name, "Test Asset")
        self.assertEqual(self.asset.total_quantity, 100)

    def test_asset_str(self):
        self.assertEqual(str(self.asset), "Activo de prueba - Units - 100")

    @patch("apps.project.specific.assets.signals.Image.open")
    def test_optimize_image_signal(self, mock_open):
        mock_img = MagicMock(spec=Image.Image)
        mock_open.return_value.__enter__.return_value = mock_img

        optimize_image(AssetModel, self.asset)
        mock_img.save.assert_called_once_with(
            self.asset.asset_img.path, quality=40, optimize=True)

    @patch("os.remove")
    def test_auto_delete_asset_img_on_delete_signal(self, mock_remove):
        # Create a mock file path
        self.asset.asset_img = "mock/path/to/image.jpg"
        self.asset.save()

        auto_delete_asset_img_on_delete(AssetModel, self.asset)
        mock_remove.assert_called_once_with("mock/path/to/image.jpg")

    @patch("os.remove")
    def test_auto_delete_asset_img_on_change_signal(self, mock_remove):
        old_image_path = "mock/path/to/old_image.jpg"
        new_image_path = "mock/path/to/new_image.jpg"
        self.asset.asset_img = old_image_path
        self.asset.save()

        # Simulate changing the image
        self.asset.asset_img = new_image_path
        self.asset.save()

        auto_delete_asset_img_on_change(AssetModel, self.asset)
        mock_remove.assert_called_once_with(old_image_path)

    def test_validate_asset_total_quantity(self):
        with patch('apps.project.specific.assets.models.AssetModel.assetlocation_asset') as mock_asset_location:
            mock_asset_location.aggregate.return_value = {'total': 50}
            self.asset.validate_asset_total_quantity()
            self.assertEqual(self.asset.total_quantity, 50)


class AssetModelSignalConnectionTestCase(TestCase):
    def test_signals_connected(self):
        self.assertTrue(post_save.has_listeners(AssetModel))
        self.assertTrue(post_delete.has_listeners(AssetModel))
        self.assertTrue(pre_save.has_listeners(AssetModel))

    def test_signals_registered_with_auditlog(self):
        from auditlog.registry import auditlog
        self.assertTrue(auditlog.contains(AssetModel))
