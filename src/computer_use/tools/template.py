"""
Template management tool for UI element templates.

Provides functionality to save, load, list, and manage UI element templates
for image-based automation.
"""

import json
import os
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from PIL.Image import Image

from ..core.config import config
from ..core.exceptions import OperationFailedError, ValidationError
from ..core.logger import get_logger
from .screen import ScreenTool

logger = get_logger(__name__)


@dataclass
class TemplateMetadata:
    """Metadata for a UI template."""
    name: str
    description: str
    created_at: str
    updated_at: str
    original_region: Optional[Tuple[int, int, int, int]] = None  # (left, top, width, height)
    original_screen_size: Optional[Tuple[int, int]] = None  # (width, height)
    tags: List[str] = None

    def __post_init__(self):
        if self.tags is None:
            self.tags = []


class TemplateManager:
    """Manages UI element templates for image-based automation."""

    # Default templates directory (project root/templates)
    DEFAULT_TEMPLATES_DIR = Path("templates")
    METADATA_FILE = "metadata.json"
    IMAGE_EXTENSIONS = [".png", ".jpg", ".jpeg"]

    def __init__(self, templates_dir: Optional[Path] = None):
        """
        Initialize TemplateManager.

        Args:
            templates_dir: Directory to store templates (defaults to ./templates)
        """
        self.templates_dir = templates_dir or self.DEFAULT_TEMPLATES_DIR
        self._ensure_templates_dir()

    def _ensure_templates_dir(self):
        """Ensure templates directory exists."""
        self.templates_dir.mkdir(parents=True, exist_ok=True)
        logger.debug(f"Using templates directory: {self.templates_dir.absolute()}")

    def _get_template_dir(self, name: str) -> Path:
        """Get the directory for a specific template."""
        return self.templates_dir / name

    def _get_metadata_path(self, name: str) -> Path:
        """Get the metadata file path for a template."""
        return self._get_template_dir(name) / self.METADATA_FILE

    def _get_image_path(self, name: str) -> Path:
        """Get the image file path for a template (checks common extensions)."""
        template_dir = self._get_template_dir(name)
        for ext in self.IMAGE_EXTENSIONS:
            img_path = template_dir / f"image{ext}"
            if img_path.exists():
                return img_path
        # Default to .png if no image exists yet
        return template_dir / "image.png"

    def save_template(
        self,
        name: str,
        image: Image,
        description: str = "",
        region: Optional[Tuple[int, int, int, int]] = None,
        tags: Optional[List[str]] = None,
    ) -> Path:
        """
        Save a UI element template.

        Args:
            name: Unique name for the template
            image: PIL Image of the UI element
            description: Description of the template
            region: Original region on screen (left, top, width, height)
            tags: List of tags for categorization

        Returns:
            Path to the saved template directory

        Raises:
            ValidationError: If name is invalid
        """
        # Validate name
        if not name or not name.strip():
            raise ValidationError("Template name cannot be empty")
        if "/" in name or "\\" in name:
            raise ValidationError("Template name cannot contain path separators")

        template_dir = self._get_template_dir(name)
        template_dir.mkdir(parents=True, exist_ok=True)

        # Save image
        img_path = self._get_image_path(name)
        image.save(img_path)
        logger.info(f"Saved template image to: {img_path}")

        # Get screen size for reference
        try:
            screen_size = ScreenTool.get_size()
        except Exception:
            screen_size = None

        # Save metadata
        now = datetime.now().isoformat()
        metadata = TemplateMetadata(
            name=name,
            description=description,
            created_at=now,
            updated_at=now,
            original_region=region,
            original_screen_size=screen_size,
            tags=tags or [],
        )

        metadata_path = self._get_metadata_path(name)
        with open(metadata_path, "w", encoding="utf-8") as f:
            json.dump(asdict(metadata), f, indent=2, ensure_ascii=False)

        logger.info(f"Saved template metadata to: {metadata_path}")
        return template_dir

    def capture_and_save_template(
        self,
        name: str,
        region: Tuple[int, int, int, int],
        description: str = "",
        tags: Optional[List[str]] = None,
    ) -> Path:
        """
        Capture a region of the screen and save as a template.

        Args:
            name: Unique name for the template
            region: Region to capture (left, top, width, height)
            description: Description of the template
            tags: List of tags for categorization

        Returns:
            Path to the saved template directory
        """
        from ..utils.validators import validate_region

        region = validate_region(region)

        logger.info(f"Capturing template '{name}' from region: {region}")
        image = ScreenTool.screenshot(region=region)

        return self.save_template(
            name=name,
            image=image,
            description=description,
            region=region,
            tags=tags,
        )

    def load_template(self, name: str) -> Tuple[Image, Optional[TemplateMetadata]]:
        """
        Load a template by name.

        Args:
            name: Name of the template to load

        Returns:
            Tuple of (PIL Image, TemplateMetadata)

        Raises:
            OperationFailedError: If template not found
        """
        template_dir = self._get_template_dir(name)
        if not template_dir.exists():
            raise OperationFailedError(f"Template not found: {name}")

        # Load image
        img_path = self._get_image_path(name)
        if not img_path.exists():
            raise OperationFailedError(f"Template image not found: {name}")

        from PIL import Image as PILImage
        image = PILImage.open(img_path)

        # Load metadata
        metadata = None
        metadata_path = self._get_metadata_path(name)
        if metadata_path.exists():
            try:
                with open(metadata_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    metadata = TemplateMetadata(**data)
            except Exception as e:
                logger.warning(f"Failed to load metadata for {name}: {e}")

        return image, metadata

    def get_template_image_path(self, name: str) -> Path:
        """
        Get the path to a template's image file.

        Args:
            name: Name of the template

        Returns:
            Path to the image file

        Raises:
            OperationFailedError: If template not found
        """
        img_path = self._get_image_path(name)
        if not img_path.exists():
            raise OperationFailedError(f"Template not found: {name}")
        return img_path

    def list_templates(self) -> List[TemplateMetadata]:
        """
        List all available templates.

        Returns:
            List of TemplateMetadata objects
        """
        templates = []

        if not self.templates_dir.exists():
            return templates

        for item in self.templates_dir.iterdir():
            if item.is_dir():
                metadata_path = item / self.METADATA_FILE
                if metadata_path.exists():
                    try:
                        with open(metadata_path, "r", encoding="utf-8") as f:
                            data = json.load(f)
                            templates.append(TemplateMetadata(**data))
                    except Exception as e:
                        logger.warning(f"Failed to load metadata for {item.name}: {e}")

        return sorted(templates, key=lambda t: t.name)

    def template_exists(self, name: str) -> bool:
        """Check if a template exists."""
        return self._get_template_dir(name).exists()

    def delete_template(self, name: str) -> bool:
        """
        Delete a template.

        Args:
            name: Name of the template to delete

        Returns:
            True if template was deleted, False if not found
        """
        import shutil

        template_dir = self._get_template_dir(name)
        if not template_dir.exists():
            return False

        shutil.rmtree(template_dir)
        logger.info(f"Deleted template: {name}")
        return True

    def update_template_metadata(
        self,
        name: str,
        description: Optional[str] = None,
        tags: Optional[List[str]] = None,
    ) -> bool:
        """
        Update template metadata.

        Args:
            name: Name of the template
            description: New description (None to keep existing)
            tags: New tags list (None to keep existing)

        Returns:
            True if updated, False if template not found
        """
        metadata_path = self._get_metadata_path(name)
        if not metadata_path.exists():
            return False

        try:
            with open(metadata_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            if description is not None:
                data["description"] = description
            if tags is not None:
                data["tags"] = tags

            data["updated_at"] = datetime.now().isoformat()

            with open(metadata_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            logger.info(f"Updated metadata for template: {name}")
            return True
        except Exception as e:
            logger.error(f"Failed to update metadata: {e}")
            return False


# Global template manager instance
_template_manager: Optional[TemplateManager] = None


def get_template_manager() -> TemplateManager:
    """Get the global TemplateManager instance."""
    global _template_manager
    if _template_manager is None:
        _template_manager = TemplateManager()
    return _template_manager


def set_template_manager(manager: TemplateManager) -> None:
    """Set the global TemplateManager instance (for testing)."""
    global _template_manager
    _template_manager = manager
