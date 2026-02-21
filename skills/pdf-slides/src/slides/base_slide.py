"""Abstract base class for all slide types."""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Optional
from reportlab.lib.units import inch
from reportlab.pdfgen.canvas import Canvas

if TYPE_CHECKING:
    from ..branding.brand_manager import BrandManager


class BaseSlide(ABC):
    """Abstract base class for all slide types.

    All slides inherit from this class and implement the render() method.
    Provides common functionality for headers, footers, and styling.
    """

    # Standard 16:9 slide dimensions (points)
    WIDTH = 10 * inch
    HEIGHT = 5.625 * inch

    # Default margins
    MARGIN_TOP = 72
    MARGIN_BOTTOM = 72
    MARGIN_LEFT = 72
    MARGIN_RIGHT = 72

    def __init__(self, data: dict, brand_manager: "BrandManager"):
        """Initialize slide with data and branding.

        Args:
            data: Slide-specific data dict from JSON outline
            brand_manager: BrandManager instance for styling
        """
        self.data = data
        self.brand = brand_manager
        self.title = data.get("title", "")

    @abstractmethod
    def render(self, canvas: Canvas) -> None:
        """Render the slide content to the canvas.

        Args:
            canvas: ReportLab Canvas to draw on
        """
        pass

    def render_header(self, canvas: Canvas) -> None:
        """Render header section with title and optional logo.

        Args:
            canvas: ReportLab Canvas to draw on
        """
        # Get brand colors and fonts
        primary_color = self.brand.get_color("primary")
        title_font = self.brand.get_font("heading")
        title_size = self.brand.get_size("heading")

        # Draw slide title
        canvas.setFillColor(primary_color)
        canvas.setFont(title_font, title_size)
        canvas.drawString(
            self.MARGIN_LEFT,
            self.HEIGHT - self.MARGIN_TOP,
            self.title
        )

        # Draw logo if configured
        if self.brand.logo_path:
            self._draw_logo(canvas)

    def render_footer(self, canvas: Canvas, page_num: int, total_pages: int) -> None:
        """Render footer section with page number.

        Args:
            canvas: ReportLab Canvas to draw on
            page_num: Current page number
            total_pages: Total number of pages
        """
        text_color = self.brand.get_color("text")
        body_font = self.brand.get_font("body")
        body_size = self.brand.get_size("body")

        # Draw page number
        canvas.setFillColor(text_color)
        canvas.setFont(body_font, body_size)
        page_text = f"Page {page_num} of {total_pages}"
        canvas.drawCentredString(
            self.WIDTH / 2,
            self.MARGIN_BOTTOM - 20,
            page_text
        )

        # Draw author/date if available from deck metadata
        author = self.brand.deck_author
        date_str = self.brand.deck_date
        if author:
            canvas.setFont(body_font, body_size)
            canvas.drawString(
                self.MARGIN_LEFT,
                self.MARGIN_BOTTOM - 20,
                author
            )

    def _draw_logo(self, canvas: Canvas) -> None:
        """Draw logo in configured position.

        Args:
            canvas: ReportLab Canvas to draw on
        """
        try:
            from reportlab.lib.utils import ImageReader

            logo_width = self.brand.logo_width
            logo_placement = self.brand.logo_placement

            # Calculate position based on placement
            if logo_placement == "top-right":
                x = self.WIDTH - self.MARGIN_RIGHT - logo_width
                y = self.HEIGHT - self.MARGIN_TOP
            elif logo_placement == "top-left":
                x = self.MARGIN_LEFT
                y = self.HEIGHT - self.MARGIN_TOP
            else:  # default top-right
                x = self.WIDTH - self.MARGIN_RIGHT - logo_width
                y = self.HEIGHT - self.MARGIN_TOP

            # Draw logo maintaining aspect ratio
            img = ImageReader(self.brand.logo_path)
            img_width, img_height = img.getSize()
            aspect_ratio = img_height / img_width
            logo_height = logo_width * aspect_ratio

            canvas.drawImage(
                img,
                x, y - logo_height,
                width=logo_width,
                height=logo_height,
                preserveAspectRatio=True,
                mask='auto'
            )
        except Exception:
            # Silently skip logo if it fails to load
            pass

    def get_content_bounds(self) -> tuple[float, float, float, float]:
        """Get the bounding box for content area.

        Returns:
            Tuple of (x, y, width, height) for content area
        """
        header_height = 100  # Space reserved for header
        footer_height = 60   # Space reserved for footer

        x = self.MARGIN_LEFT
        y = self.MARGIN_BOTTOM + footer_height
        width = self.WIDTH - self.MARGIN_LEFT - self.MARGIN_RIGHT
        height = self.HEIGHT - self.MARGIN_TOP - self.MARGIN_BOTTOM - header_height

        return (x, y, width, height)
