"""Color palette management for slide branding."""

from typing import Optional
from reportlab.lib.colors import HexColor, Color


class ColorPalette:
    """Manages color scheme for slide decks.

    Handles color definitions, conversion between formats,
    and provides access to branded color sets.
    """

    DEFAULT_COLORS = {
        "primary": "#2E5BFF",
        "secondary": "#6C7A9C",
        "accent": "#00D9A0",
        "background": "#FFFFFF",
        "text": "#1A1A2E",
        "text_light": "#6C7A9C",
        "border": "#E0E0E0",
        "success": "#00D9A0",
        "warning": "#FFB800",
        "error": "#FF6B6B",
    }

    DEFAULT_CHART_COLORS = [
        "#2E5BFF",  # Primary blue
        "#00D9A0",  # Accent green
        "#FFB800",  # Warning yellow
        "#FF6B6B",  # Error red
        "#9B59B6",  # Purple
        "#3498DB",  # Light blue
        "#1ABC9C",  # Teal
        "#E74C3C",  # Red
    ]

    def __init__(self, custom_colors: Optional[dict] = None):
        """Initialize color palette.

        Args:
            custom_colors: Optional dict of color names to hex values
        """
        self.colors = self.DEFAULT_COLORS.copy()
        self.chart_colors = self.DEFAULT_CHART_COLORS.copy()

        if custom_colors:
            self.colors.update(custom_colors.get("colors", {}))

            # Override chart colors if provided
            if "chart_colors" in custom_colors:
                self.chart_colors = custom_colors["chart_colors"]

    def get_color(self, name: str) -> Color:
        """Get a ReportLab Color object by name.

        Args:
            name: Color name (e.g., 'primary', 'secondary', 'accent')

        Returns:
            ReportLab Color object

        Raises:
            KeyError: If color name not found
        """
        hex_value = self.colors.get(name)
        if not hex_value:
            raise KeyError(f"Color '{name}' not found in palette")
        return HexColor(hex_value)

    def get_chart_color(self, index: int) -> Color:
        """Get a color from the chart palette by index.

        Args:
            index: Index into chart color palette (cycles if exceeds length)

        Returns:
            ReportLab Color object
        """
        hex_value = self.chart_colors[index % len(self.chart_colors)]
        return HexColor(hex_value)

    def get_hex(self, name: str) -> str:
        """Get hex string value for a color.

        Args:
            name: Color name

        Returns:
            Hex color string (e.g., '#2E5BFF')
        """
        return self.colors.get(name, self.DEFAULT_COLORS.get(name, "#000000"))

    def get_chart_hex(self, index: int) -> str:
        """Get hex string from chart palette by index.

        Args:
            index: Index into chart color palette

        Returns:
            Hex color string
        """
        return self.chart_colors[index % len(self.chart_colors)]

    def add_color(self, name: str, hex_value: str) -> None:
        """Add a custom color to the palette.

        Args:
            name: Name for the color
            hex_value: Hex color value (e.g., '#FF5733')
        """
        if not hex_value.startswith("#"):
            hex_value = f"#{hex_value}"
        self.colors[name] = hex_value

    def to_dict(self) -> dict:
        """Export palette as dictionary.

        Returns:
            Dict with colors and chart_colors
        """
        return {
            "colors": self.colors.copy(),
            "chart_colors": self.chart_colors.copy(),
        }
