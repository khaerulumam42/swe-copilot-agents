"""Two-column slide implementation."""

from typing import Dict, Any
from reportlab.pdfgen.canvas import Canvas

from .base_slide import BaseSlide


class TwoColumnSlide(BaseSlide):
    """Slide with two side-by-side content columns.

    Useful for comparisons, before/after, or related content.
    """

    def render(self, canvas: Canvas) -> None:
        """Render the two-column slide.

        Args:
            canvas: ReportLab Canvas to draw on
        """
        # Render header
        self.render_header(canvas)

        # Get content area
        x, y, width, height = self.get_content_bounds()

        # Get brand styling
        primary_color = self.brand.get_color("primary")
        secondary_color = self.brand.get_color("secondary")
        text_color = self.brand.get_color("text")
        accent_color = self.brand.get_color("accent")

        heading_font = self.brand.get_font("subheading")
        heading_size = self.brand.get_size("subheading")

        body_font = self.brand.get_font("body")
        body_size = self.brand.get_size("body")

        # Calculate column dimensions
        col_width = (width - 40) / 2  # 20pt gap between columns
        left_x = x
        right_x = x + col_width + 40

        # Get column data
        left_data = self.data.get("left", {})
        right_data = self.data.get("right", {})

        # Draw divider line
        canvas.setStrokeColor(accent_color)
        canvas.setLineWidth(2)
        canvas.line(x + width / 2, y, x + width / 2, y + height)

        # Render left column
        self._render_column(
            canvas,
            left_data,
            left_x,
            y,
            col_width,
            height,
            heading_font,
            heading_size,
            body_font,
            body_size,
            primary_color,
            text_color,
            accent_color,
        )

        # Render right column
        self._render_column(
            canvas,
            right_data,
            right_x,
            y,
            col_width,
            height,
            heading_font,
            heading_size,
            body_font,
            body_size,
            primary_color,
            text_color,
            accent_color,
        )

        # Render footer
        self.render_footer(canvas, 0, 0)  # Page numbers set by generator

    def _render_column(
        self,
        canvas: Canvas,
        column_data: Dict[str, Any],
        x: float,
        y: float,
        width: float,
        height: float,
        heading_font: str,
        heading_size: int,
        body_font: str,
        body_size: int,
        primary_color,
        text_color,
        accent_color,
    ) -> None:
        """Render a single column.

        Args:
            canvas: ReportLab Canvas
            column_data: Column data dict with title and content
            x, y, width, height: Column bounds
            heading_font, heading_size: Heading font settings
            body_font, body_size: Body font settings
            primary_color, text_color: Text colors
            accent_color: Accent color
        """
        current_y = y + height - heading_size

        # Draw column heading if present
        if "title" in column_data:
            canvas.setFillColor(primary_color)
            canvas.setFont(heading_font, heading_size)
            canvas.drawString(x, current_y, column_data["title"])
            current_y -= heading_size * 1.5

        # Draw bullet points
        points = column_data.get("points", [])
        line_spacing = body_size * 1.8

        for point in points:
            # Draw bullet
            canvas.setFillColor(accent_color)
            canvas.setFont(body_font, body_size)
            canvas.drawString(x, current_y, "•")

            # Draw text with indent
            canvas.setFillColor(text_color)
            canvas.drawString(x + 20, current_y, point)
            current_y -= line_spacing
