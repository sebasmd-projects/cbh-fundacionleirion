# Assets Application

## Table of Contents

- [Assets Application](#assets-application)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Usage](#usage)
  - [Models](#models)
    - [`AssetModel`](#assetmodel)
  - [Signals](#signals)
    - [`optimize_image`](#optimize_image)
    - [`assets_directory_path`](#assets_directory_path)
    - [`auto_delete_asset_img_on_delete`](#auto_delete_asset_img_on_delete)
    - [`auto_delete_asset_img_on_change`](#auto_delete_asset_img_on_change)
  - [Admin Interface](#admin-interface)
  - [Testing](#testing)
  - [Localization](#localization)
  - [License](#license)

## Overview

The Assets application manages the inventory of assets within the project. It includes the ability to track assets, their quantities, locations, and associated categories. The application integrates with Django's admin interface and provides signals to handle image optimization and deletion automatically.

  ```cmd
  |   apps.py
  |   assets.txt
  |   models.py
  |   signals.py
  |   tests.py
  |   urls.py
  |   views.py
  |   __init__.py
  |
  +---admin
  |   |   actions.py
  |   |   filters.py
  |   |   forms.py
  |   |   inline.py
  |   |   resources.py
  |   |   __init__.py
  |   |
  |
  +---locale
  |   \---es
  |       \---LC_MESSAGES
  |               django.mo
  |               django.po
  |
  ```

## Usage

To use the application, install the necessary requirements, migrate the database, and create an admin user. The admin interface allows for the management of assets, including adding, editing, and deleting records.

## Models

### `AssetModel`

- **Fields**:
  - `asset_img`: Image field for the asset's image.
  - `observations`: Text field for additional notes or observations.
  - `units_per_box`: Number of units per box.
  - `boxes_per_container`: Number of boxes per container.
  - `name`: English name of the asset.
  - `es_name`: Spanish name of the asset.
  - `category`: Foreign key linking to the `AssetCategoryModel`.
  - `description`: Text field for a detailed description.
  - `asset_year`: The year associated with the asset.
  - `emission`: The emission identifier for the asset.
  - `quantity_type`: Char field for the type of quantity (Units, Containers, Boxes, Other).
  - `total_quantity`: Total quantity of the asset in stock.

- **Utility**:
  - The `AssetModel` represents individual assets and includes methods to validate and ensure that the total quantity is consistent with related asset locations. It also connects to signals to handle image optimization and deletion.

## Signals

### `optimize_image`

Optimizes the image quality and size after saving the model.

### `assets_directory_path`

Generates a unique file path for storing asset images based on the asset's name and the current date.

### `auto_delete_asset_img_on_delete`

Deletes the image file from the filesystem when the corresponding `AssetModel` instance is deleted.

### `auto_delete_asset_img_on_change`

Deletes the old image file from the filesystem when the corresponding `AssetModel` instance is updated with a new file.

## Admin Interface

The admin interface allows users to manage assets with advanced filtering, inline editing of related locations, and export/import functionality. Key features include:

- **Actions**:
  - `update_total_quantities`: Recalculates and updates the total quantities of selected assets.
- **Filters**:
  - `ZeroTotalQuantityFilter`: Filters assets based on whether their total quantity is zero.
  - `ZeroUnitsPerBoxFilter`: Filters assets based on whether their units per box is zero.
  - `ZeroBoxesPerContainerFilter`: Filters assets based on whether their boxes per container is zero.
  - `ParentCategoryFilter`: Filters assets based on their parent category.
- **Inlines**:
  - `AssetLocationInline`: Inline editing for related asset locations.

## Testing

Tests are located in the `tests.py` file and cover the core functionalities of the `AssetModel`, including signals and admin actions.

## Localization

The application supports localization, with Spanish translations available for all user-facing text. Translation files are located in the `locale/es/LC_MESSAGES` directory.

## License

TODO
