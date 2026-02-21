"""Brand manager for loading and managing branding configuration."""

from pathlib import Path
from typing import TYPE_CHECKING, Optional
import yaml

from .color_palette import ColorPalette

if TYPE_CHECKING:
    from reportlab.pdfbase.pdfmetrics import Font


class BrandManager:
    """Manages branding configuration for slide decks.

    Handles loading branding from YAML files or inline JSON,
    manages colors, fonts, logos, and provides access to
    brand styling options.

    Priority: inline config > file config > defaults
    """

    DEFAULT_SIZES = {
        "title": 48,
        "heading": 32,
        "subheading": 24,
        "body": 18,
        "caption": 14,
    }

    DEFAULT_FONTS = {
        "title": "Helvetica-Bold",
        "heading": "Helvetica-Bold",
        "subheading": "Helvetica-Bold",
        "body": "Helvetica",
        "caption": "Helvetica",
    }

    def __init__(
        self,
        config_path: Optional[str | Path] = None,
        inline_branding: Optional[dict] = None,
    ):
        """Initialize BrandManager.

        Args:
            config_path: Optional path to YAML branding config file
            inline_branding: Optional inline branding dict from JSON outline
        """
        self.config_path = Path(config_path) if config_path else None
        self.inline_branding = inline_branding or {}

        # Load configuration
        self._load_config()

    def _load_config(self) -> None:
        """Load branding configuration from file and/or inline config."""
        # Start with defaults
        self.colors = ColorPalette()
        self.fonts = self.DEFAULT_FONTS.copy()
        self.sizes = self.DEFAULT_SIZES.copy()

        # Layout defaults
        self.logo_path: Optional[str] = None
        self.logo_width = 120
        self.logo_placement = "top-right"

        # Deck metadata
        self.deck_author: Optional[str] = None
        self.deck_date: Optional[str] = None

        # Load from file if provided
        if self.config_path and self.config_path.exists():
            self._load_from_yaml()

        # Apply inline branding (highest priority)
        if self.inline_branding:
            self._apply_inline_branding()

    def _load_from_yaml(self) -> None:
        """Load branding configuration from YAML file."""
        try:
            with open(self.config_path, "r") as f:
                config = yaml.safe_load(f) or {}

            # Apply colors
            if "colors" in config:
                self.colors = ColorPalette(config["colors"])

            # Apply fonts
            if "typography" in config:
                typography = config["typography"]
                if "fonts" in typography:
                    self.fonts.update(typography["fonts"])
                if "sizes" in typography:
                    self.sizes.update(typography["sizes"])

            # Apply layout
            if "layout" in config:
                layout = config["layout"]
                if "logo" in layout:
                    logo = layout["logo"]
                    if "placement" in logo:
                        self.logo_placement = logo["placement"]
                    if "width" in logo:
                        self.logo_width = logo["width"]
                    if "path" in logo:
                        self.logo_path = logo["path"]

        except Exception:
            # Use defaults if YAML loading fails
            pass

    def _apply_inline_branding(self) -> None:
        """Apply inline branding from JSON outline."""
        branding = self.inline_branding

        # Apply colors
        if "colors" in branding or any(
            k.endswith("_color") for k in branding
        ):
            color_dict = {}
            for key, value in branding.items():
                if key.endswith("_color"):
                    name = key.replace("_color", "")
                    color_dict[name] = value
                elif key == "colors":
                    color_dict.update(value)
            if color_dict:
                self.colors = ColorPalette(color_dict)

        # Apply logo
        if "logo_path" in branding:
            self.logo_path = branding["logo_path"]
        if "logo_width" in branding:
            self.logo_width = branding["logo_width"]
        if "logo_placement" in branding:
            self.logo_placement = branding["logo_placement"]

        # Apply custom fonts if provided
        if "fonts" in branding:
            self.fonts.update(branding["fonts"])

        # Apply sizes if provided
        if "sizes" in branding:
            self.sizes.update(branding["sizes"])

        # Store deck metadata
        if "author" in branding:
            self.deck_author = branding["author"]
        if "date" in branding:
            self.deck_date = branding.get("date")

    def get_color(self, name: str):
        """Get a ReportLab Color by name.

        Args:
            name: Color name from palette

        Returns:
            ReportLab Color object
        """
        return self.colors.get_color(name)

    def get_font(self, role: str) -> str:
        """Get font name for a text role.

        Args:
            role: Text role (title, heading, body, etc.)

        Returns:
            Font name string
        """
        return self.fonts.get(role, self.DEFAULT_FONTS.get(role, "Helvetica"))

    def get_size(self, role: str) -> int:
        """Get font size for a text role.

        Args:
            role: Text role (title, heading, body, etc.)

        Returns:
            Font size in points
        """
        return self.sizes.get(role, self.DEFAULT_SIZES.get(role, 18))

    def register_custom_font(self, font_name: str, font_path: str) -> None:
        """Register a custom TrueType or OpenType font.

        Args:
            font_name: Name to reference the font
            font_path: Path to TTF or OTF font file
        """
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.ttfonts import TTFont

        try:
            font_path_obj = Path(font_path)
            if font_path_obj.exists():
                pdfmetrics.registerFont(TTFont(font_name, str(font_path_obj)))
                # Update font mapping
                self.fonts["body"] = font_name
        except Exception:
            pass

    def to_dict(self) -> dict:
        """Export branding configuration as dict.

        Returns:
            Dictionary representation of current branding
        """
        return {
            "colors": self.colors.to_dict(),
            "fonts": self.fonts.copy(),
            "sizes": self.sizes.copy(),
            "logo": {
                "path": self.logo_path,
                "width": self.logo_width,
                "placement": self.logo_placement,
            } if self.logo_path else None,
        }
