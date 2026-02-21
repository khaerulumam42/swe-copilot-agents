"""Section divider slide implementation."""

from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.units import inch

from .base_slide import BaseSlide


class SectionSlide(BaseSlide):
    """Section divider slide.

    Used to separate major sections in a presentation.
    Displays a large section number or title with minimal decoration.
    """

    def render(self, canvas: Canvas) -> None:
        """Render the section slide.

        Args:
            canvas: ReportLab Canvas to draw on
        """
        # Get brand styling
        primary_color = self.brand.get_color("primary")
        secondary_color = self.brand.get_color("secondary")
        accent_color = self.brand.get_color("accent")

        title_font = self.brand.get_font("title")
        title_size = self.brand.get_size("title")

        # Calculate center position
        center_x = self.WIDTH / 2
        center_y = self.HEIGHT / 2

        # Draw large section number if present
        section_number = self.data.get("section_number", "")
        if section_number:
            # Draw very large semi-transparent number in background
            canvas.setFillColor(secondary_color)
            canvas.setFont(title_font, title_size * 3)
            canvas.drawCentredString(center_x, center_y + title_size, section_number)

        # Draw section title
        canvas.setFillColor(primary_color)
        canvas.setFont(title_font, title_size)

        # Center the title
        title_width = canvas.stringWidth(self.title, title_font, title_size)
        canvas.drawCentredString(
            center_x,
            center_y - title_size * 0.5,
            self.title
        )

        # Draw decorative accent line
        canvas.setFillColor(accent_color)
        line_width = min(200, self.WIDTH - 200)
        canvas.rect(
            (self.WIDTH - line_width) / 2,
            center_y - title_size * 0.8,
            line_width,
            4,
            fill=True,
            stroke=False,
        )

        # Optional subtitle
        subtitle = self.data.get("subtitle", "")
        if subtitle:
            subtitle_font = self.brand.get_font("subheading")
            subtitle_size = self.brand.get_size("subheading")
            canvas.setFillColor(secondary_color)
            canvas.setFont(subtitle_font, subtitle_size)
            canvas.drawCentredString(
                center_x,
                center_y - title_size * 1.2,
                subtitle
            )

        # Draw logo if configured (smaller, in corner)
        if self.brand.logo_path:
            self._draw_corner_logo(canvas)
