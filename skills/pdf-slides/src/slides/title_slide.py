"""Title slide implementation."""

from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.units import inch

from .base_slide import BaseSlide


class TitleSlide(BaseSlide):
    """Title/cover slide with title, subtitle, and optional author info.

    Typically used as the first slide in a deck.
    """

    def render(self, canvas: Canvas) -> None:
        """Render the title slide.

        Args:
            canvas: ReportLab Canvas to draw on
        """
        # Get brand styling
        primary_color = self.brand.get_color("primary")
        secondary_color = self.brand.get_color("secondary")
        accent_color = self.brand.get_color("accent")

        title_font = self.brand.get_font("title")
        title_size = self.brand.get_size("title")

        heading_font = self.brand.get_font("subheading")
        heading_size = self.brand.get_size("subheading")

        body_font = self.brand.get_font("body")
        body_size = self.brand.get_size("body")

        # Draw logo if configured
        if self.brand.logo_path:
            self._draw_logo(canvas)

        # Calculate vertical center for title
        center_y = self.HEIGHT / 2

        # Draw subtitle (if present)
        subtitle = self.data.get("subtitle", "")
        if subtitle:
            canvas.setFillColor(secondary_color)
            canvas.setFont(heading_font, heading_size)
            subtitle_width = canvas.stringWidth(subtitle, heading_font, heading_size)
            canvas.drawCentredString(
                self.WIDTH / 2,
                center_y + title_size * 0.7,
                subtitle
            )

        # Draw title
        canvas.setFillColor(primary_color)
        canvas.setFont(title_font, title_size)
        canvas.drawCentredString(
            self.WIDTH / 2,
            center_y - title_size * 0.3,
            self.title
        )

        # Draw accent line below title
        canvas.setFillColor(accent_color)
        line_width = 100
        canvas.rect(
            (self.WIDTH - line_width) / 2,
            center_y - title_size * 0.5 - 10,
            line_width,
            4,
            fill=True,
            stroke=False,
        )

        # Draw author and date at bottom
        author = self.data.get("author", self.brand.deck_author)
        date = self.data.get("date", self.brand.deck_date)

        if author or date:
            canvas.setFillColor(secondary_color)
            canvas.setFont(body_font, body_size)

            if author and date:
                text = f"{author} | {date}"
            elif author:
                text = author
            else:
                text = date

            canvas.drawCentredString(
                self.WIDTH / 2,
                self.MARGIN_BOTTOM,
                text
            )
