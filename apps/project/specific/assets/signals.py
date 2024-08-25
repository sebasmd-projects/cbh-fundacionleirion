import hashlib
import os
from datetime import date

from django.db import transaction
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from PIL import Image


def optimize_image(sender, instance, *args, **kwargs):
    """
    This function is used as a signal handler for the post_save signal of a model with an asset_img field.
    It opens the image file, saves it with a quality of 40 and optimizes the image.
    """
    if instance.asset_img:
        asset_img = Image.open(
            instance.asset_img.path
        )
        asset_img.save(
            instance.asset_img.path,
            quality=40,
            optimize_image=True
        )


def generate_md5_hash(value: str):
    """
    Generates an MD5 hash for the given value.
    """
    return hashlib.md5(value.encode('utf-8')).hexdigest()


def assets_directory_path(instance, filename):
    """
    Generates a file path for an asset image.
    The path includes the current year, month, and day, and the hash of the filename without the extension.
    Maintains the original file extension.
    """
    es_name = slugify(instance.es_name)[:40]
    base_filename, file_extension = os.path.splitext(filename)
    filename_hash = generate_md5_hash(base_filename)
    return f"asset/{es_name}/img/{date.today().year}/{date.today().month}/{date.today().day}/{filename_hash[:10]}{file_extension}"


def auto_delete_asset_img_on_delete(sender, instance, *args, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `AssetModel` object is deleted.
    """
    if instance.asset_img:
        if os.path.isfile(instance.asset_img.path):
            os.remove(instance.asset_img.path)


def auto_delete_asset_img_on_change(sender, instance, *args, **kwargs):
    """
    Deletes old file from filesystem when corresponding `AssetModel` object is updated with new file.
    """
    if instance.pk:  # Check if the instance is already saved (i.e., has a primary key)
        try:
            old_instance = sender.objects.get(
                pk=instance.pk
            )  # Get the old instance
        except sender.DoesNotExist:
            return  # If old instance doesn't exist, do nothing
        if old_instance.asset_img != instance.asset_img:  # Check if profile photo has changed
            if old_instance.asset_img:  # Check if there was an old profile photo
                if os.path.isfile(old_instance.asset_img.path):  # Check if old file exists
                    os.remove(old_instance.asset_img.path)  # Delete old file


def return_asset_total_quantity_on_delete(sender, instance, **kwargs):
    from apps.project.specific.assets.models import AssetModel

    asset = instance.assets

    with transaction.atomic():
        if instance.status != 'A':
            asset.total_quantity += instance.quantity
            asset.save()
