
import logging
import os
from datetime import date

from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from PIL import Image

from app_core import generate_md5_hash

logger = logging.getLogger(__name__)


def optimize_image(sender, instance, *args, **kwargs):
    """
    Optimize image quality and size after saving the model.
    """
    if instance.asset_img:
        img_path = instance.asset_img.path
        try:
            with Image.open(img_path) as img:
                img.save(img_path, quality=40, optimize=True)
        except Exception as e:
            logger.error(
                f"Error optimizing image {img_path}: {e}"
            )


def assets_directory_path(instance, filename) -> str:
    """
    Generate a file path for an asset image.
    Path format: asset/{slugified_name}/img/YYYY/MM/DD/{hashed_filename}.{extension}
    """
    try:
        es_name = slugify(instance.es_name)[:40]
        base_filename, file_extension = os.path.splitext(filename)
        filename_hash = generate_md5_hash(base_filename)
        path = os.path.join(
            "asset", es_name, "img",
            str(date.today().year),
            str(date.today().month),
            str(date.today().day),
            f"{filename_hash[:10]}{file_extension}"
        )
        return path
    except Exception as e:
        logger.error(
            f"Error generating file path for {filename}: {e}"
        )
        raise e


def auto_delete_asset_img_on_delete(sender, instance, *args, **kwargs):
    """
    Delete image file from filesystem when the corresponding AssetModel instance is deleted.
    """
    if instance.asset_img:
        try:
            if os.path.isfile(instance.asset_img.path):
                os.remove(instance.asset_img.path)
        except Exception as e:
            logger.error(
                f"Error deleting image {instance.asset_img.path}: {e}"
            )


def auto_delete_asset_img_on_change(sender, instance, *args, **kwargs):
    """
    Delete old image file from filesystem when the corresponding AssetModel instance is updated with a new file.
    """
    if not instance.pk:
        return

    try:
        old_instance = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        return

    if old_instance.asset_img and old_instance.asset_img != instance.asset_img:
        try:
            if os.path.isfile(old_instance.asset_img.path):
                os.remove(old_instance.asset_img.path)
        except Exception as e:
            logger.error(
                f"Error deleting old image {old_instance.asset_img.path}: {e}"
            )
